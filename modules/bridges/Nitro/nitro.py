import asyncio
import logging

import aiohttp
from decimal import Decimal

import w3.utils
from models.interfaces.ibridge import IBridge
from w3.core.client import Client

logger = logging.getLogger(__name__)

ZERO_ADDRESS = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'
NITRO_API_QUOTE_URL = 'https://api-beta.pathfinder.routerprotocol.com/api/v2/quote'
NITRO_API_TX_URL = 'https://api-beta.pathfinder.routerprotocol.com/api/v2/transaction'


class Nitro(IBridge):

    async def bridge(self) -> dict:
        token_in = self._params.token.address or ZERO_ADDRESS
        token_out = self._params.to_network.get_token_by_symbol(self._params.token.symbol).address or ZERO_ADDRESS
        quote = await self._get_quote(token_in, token_out)
        if not quote:
            raise ValueError("No quote available for this route.")

        tx_data = await self._build_transaction(quote)
        if not tx_data:
            raise ValueError("Failed to retrieve transaction data.")

        tx_data = tx_data['txn']

        if token_in != ZERO_ADDRESS:
            token_contract = self._client.contracts.get_erc20_contract(self._params.token.address)
            spender = tx_data['to']
            amount = int(self._params.amount * 10 ** (await token_contract.functions.decimals().call()))
            await self.approve_token(self._client, token_contract, w3.utils.to_checksum_address(spender), amount)

        await self._client.transactions.send(
            encoded_data=tx_data['data'],
            contract_address=w3.utils.to_checksum_address(tx_data['to']),
            tx_value=int(tx_data['value'], 16)
        )

        logger.info(f"Bridge successful: {self._params.amount} {self._params.token.symbol} from {self._params.from_network.name} to {self._params.to_network.name}")

        return {
            'token': self._params.token.symbol,
            'from_network': self._params.from_network.name,
            'to_network': self._params.to_network.name,
            'amount': self._params.amount
        }

    async def _get_quote(self, token_in, token_out) -> dict:
        token_in_address = w3.utils.to_checksum_address(token_in)

        if token_in == ZERO_ADDRESS:
            decimals = 18
        else:
            token_contract = self._client.contracts.get_erc20_contract(token_in_address)
            decimals = await token_contract.functions.decimals().call()

        amount_in_smallest_unit = int(self._params.amount * (10 ** decimals))

        async with aiohttp.ClientSession() as session:
            async with session.get(NITRO_API_QUOTE_URL, params={
                'fromTokenAddress': token_in_address,
                'toTokenAddress': w3.utils.to_checksum_address(token_out),
                'amount': amount_in_smallest_unit,
                'fromTokenChainId': self._params.from_network.chain_id,
                'toTokenChainId': self._params.to_network.chain_id,
                'partnerId': 1,
                'slippageTolerance': 1,
                'destFuel': 0
            },proxy=self._client.w3.proxy) as response:
                response.raise_for_status()
                return await response.json()

    async def _build_transaction(self, quote: dict) -> dict:
        quote.update({
            'receiverAddress': self._client.wallet.public_key,
            'senderAddress': self._client.wallet.public_key
        })

        async with aiohttp.ClientSession() as session:
            async with session.post(NITRO_API_TX_URL, json=quote, proxy=self._client.w3.proxy) as response:
                response.raise_for_status()
                return await response.json()

    async def approve_token(self, client, token_contract, spender, amount):
        owner = client.wallet.public_key
        current_allowance = await token_contract.functions.allowance(owner, spender).call()
        decimals = await token_contract.functions.decimals().call()
        logger.info(f"Current allowance: {current_allowance/10 ** decimals}")

        if current_allowance >= amount:
            logger.info("Allowance is sufficient, no need to approve.")
            return

        encoded_data = token_contract.encode_abi(
            'approve',
            args=[spender, amount]
        )
        await self._client.transactions.send(encoded_data, token_contract.address)
        logger.info(f"Approved token: {token_contract.address}")