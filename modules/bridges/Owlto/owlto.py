import asyncio
import logging
import aiohttp
from models.interfaces.ibridge import IBridge
from w3.core.client import Client
from models.params.bridge_params import BridgeParams

logger = logging.getLogger(__name__)


class Owlto(IBridge):
    def __init__(self, client: Client, params: BridgeParams):
        super().__init__(client, params)

    async def bridge(self) -> dict:
        """Main bridge function."""
        data = await self._get_bridge_data()

        if data.get('status', {}).get('code') != 0:
            raise ValueError(f"Error retrieving data for transaction: {data['status']['message']}")

        self.tx_hash = await self._execute_bridge_transactions(data)

        await asyncio.sleep(7)  # Wait for the transaction to be processed
        result = await self.verify()

        if result:
            logger.info("Bridge verified successfully!")
        else:
            raise logger.error("Transaction verification failed.")

        return {
            'token': self._params.token,
            'from_network': self._params.from_network.name,
            'to_network': self._params.to_network.name,
            'amount': self._params.amount
        }

    async def _get_bridge_data(self) -> dict:
        """Fetch data via Owlto API."""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    "https://owlto.finance/api/bridge_api/v1/get_build_tx",
                    json={
                        "from_address": self._client.wallet.public_key,
                        "from_chain_name": self._params.from_network.name,
                        "to_address": self._client.wallet.public_key,
                        "to_chain_name": self._params.to_network.name,
                        "token_name": self._params.token,
                        "ui_value": self._params.amount,
                        "value_include_gas_fee": 'true',
                    },
                    proxy=self._client.w3.proxy
            ) as response:
                response.raise_for_status()
                return await response.json()

    async def _execute_bridge_transactions(self, data: dict):
        """Execute approve and transfer transactions."""
        approve_body = data['data']['txs'].get('approve_body')
        transfer_body = data['data']['txs'].get('transfer_body')
        to_approve = approve_body.get('to') if approve_body else None
        to_transfer = transfer_body.get('to') if transfer_body else None

        if approve_body:
            await self._client.transactions.send(encoded_data=approve_body, contract_address=to_approve, tx_value=0)
            logger.info("Approve transaction sent successfully!")
        else:
            logger.info("No approve transaction required.")

        transfer_tx_hash = await self._client.transactions.send(encoded_data=transfer_body, contract_address=to_transfer, tx_value=0)
        logger.info("Transfer transaction sent successfully!")
        return transfer_tx_hash

    async def verify(self) -> bool:
        """Verify receipt of funds via API."""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    "https://owlto.finance/api/bridge_api/v1/get_receipt",
                    json={"from_chain_hash": self.tx_hash},
                    proxy=self._client.w3.proxy
            ) as response:
                response.raise_for_status()
                receipt_data = await response.json()
                return receipt_data['status']['code'] == 0
