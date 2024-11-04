import asyncio
import logging
import aiohttp
from models.interfaces.ibridge import IBridge
from w3.core.client import Client
from models.params.bridge_params import BridgeParams
from modules.bridges.Owlto.config_owlto import NETWORK_MAPPING

logger = logging.getLogger(__name__)


class Owlto(IBridge):

    async def bridge(self) -> dict:
        """Main bridge function."""
        data = await self._get_bridge_data()

        if data['status']['code'] != 0:
            raise ValueError(f"Error retrieving data for transaction: {data['status']['message']}")

        self.tx_hash = await self._execute_bridge_transactions(data)

        logger.info(f"Bridge successful: {self._params.amount} {self._params.token.symbol} from {self._params.from_network.name} to {self._params.to_network.name}")

        return {
            'token': self._params.token.symbol,
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
                        "from_chain_name": NETWORK_MAPPING.get(str(self._params.from_network.name), str(self._params.from_network.name)),
                        "to_address": self._client.wallet.public_key,
                        "to_chain_name": NETWORK_MAPPING.get(str(self._params.to_network.name), str(self._params.to_network.name)),
                        "token_name": str(self._params.token.symbol),
                        "ui_value": str(self._params.amount),
                        "value_include_gas_fee": True,
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
        value_approve = approve_body.get('value') if approve_body else None
        value_transfer = transfer_body.get('value') if transfer_body else None

        if approve_body:
            await self._client.transactions.send(encoded_data=approve_body['data'], contract_address=self._client.w3.async_w3.to_checksum_address(to_approve), tx_value=int(value_approve))
            logger.info("Approve transaction sent successfully!")
        else:
            logger.info("No approve transaction required.")

        transfer_tx_hash = await self._client.transactions.send(encoded_data=transfer_body['data'], contract_address=self._client.w3.async_w3.to_checksum_address(to_transfer), tx_value=int(value_transfer))
        logger.info("Transfer transaction sent successfully!")
        return transfer_tx_hash['transactionHash'].hex()

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
