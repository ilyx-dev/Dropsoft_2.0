import asyncio
import logging
from decimal import Decimal
import aiohttp
import w3.utils
from models.interfaces.ibridge import IBridge
from w3.core.client import Client

logger = logging.getLogger(__name__)
ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'


class Relay(IBridge):

    async def bridge(self) -> dict:
        amount = self._params.amount
        from_token_address = self._params.token.address or ZERO_ADDRESS
        from_token = w3.utils.to_checksum_address(from_token_address)
        wallet = self._client.wallet.public_key

        if from_token != ZERO_ADDRESS:
            token_contract = self._client.contracts.get_erc20_contract(from_token)
            decimals = await token_contract.functions.decimals().call()
        else:
            decimals = 18

        amount = int(amount * (10 ** decimals))

        response_data = await self._get_quote(
            from_chain_id=self._params.from_network.chain_id,
            to_chain_id=self._params.to_network.chain_id,
            wallet=wallet,
            amount=amount
        )

        if not response_data:
            logger.error("Route not available. Please check available routes on the site.")
            raise ValueError("No available bridge route found.")

        first_step = response_data['steps'][0]
        if first_step['id'] == 'approve':
            approve_data = first_step['items'][0]['data']
            await self._send_approve_transaction(approve_data)

        elif first_step['id'] == 'deposit':
            deposit_data = first_step['items'][0]['data']
            await self._send_transaction(deposit_data)

        else:
            logger.error("Unknown first step in transaction sequence.")
            raise ValueError("Unexpected first step in transaction route.")

        swap_step = response_data['steps'][1 if first_step['id'] == 'approve' else 0]
        swap_data = swap_step['items'][0]['data']
        await self._send_transaction(swap_data)

        return {
            'token': self._params.token.symbol,
            'from_network': self._params.from_network.name,
            'to_network': self._params.to_network.name,
            'amount': self._params.amount
        }

    async def _get_quote(self, from_chain_id, to_chain_id, wallet, amount):
        originCurrency = self._params.token.address or ZERO_ADDRESS
        destinationCurrency = self._params.to_network.get_token_by_symbol(self._params.token.symbol).address or ZERO_ADDRESS
        url = "https://api.relay.link/quote"

        params = {
            'user': wallet,
            'originChainId': from_chain_id,
            'destinationChainId': to_chain_id,
            'originCurrency': w3.utils.to_checksum_address(originCurrency),
            'destinationCurrency': w3.utils.to_checksum_address(destinationCurrency),
            'recipient': wallet,
            'tradeType': 'EXACT_INPUT',
            'amount': amount,
            'referrer': 'relay.link/swap',
            'useExternalLiquidity': False,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, json=params, proxy=self._client.w3.proxy) as response:
                response.raise_for_status()
                response_data = await response.json()
                return response_data

    async def _send_approve_transaction(self, approve_data):
        logger.info("Sending approval transaction")
        await self._client.transactions.send(
            encoded_data=approve_data['data'],
            contract_address=w3.utils.to_checksum_address(approve_data['to']),
            tx_value=int(approve_data['value'])
        )
        logger.info("Approval transaction completed successfully.")

    async def _send_transaction(self, tx_data):
        """Send the transaction with provided `tx_data`."""
        await self._client.transactions.send(
            encoded_data=tx_data['data'],
            contract_address=w3.utils.to_checksum_address(tx_data['to']),
            tx_value=int(tx_data['value'])
        )
        logger.info("Transaction sent successfully.")
