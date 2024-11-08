import logging
import aiohttp
import w3.utils

from .config_base import *
from models.interfaces.iswap import ISwap

logger = logging.getLogger(__name__)


class BaseSwap(ISwap):

    async def swap(self) -> dict:
        client = self._client
        chain_id = self._params.network.chain_id
        amount = self._params.amount
        token_from = self._params.from_token
        token_to = self._params.to_token
        my_address = w3.utils.to_checksum_address(client.wallet.public_key)

        token_from_address = w3.utils.to_checksum_address(token_from.address if token_from.address else ETH_ADDRESS)
        token_to_address = w3.utils.to_checksum_address(token_to.address if token_to.address else ETH_ADDRESS)

        token_contract = self._client.contracts.get_erc20_contract(token_from_address)
        erc20_contract = client.contracts.get_erc20_contract(token_from_address)
        decimals = await erc20_contract.functions.decimals().call() if token_from_address != ETH_ADDRESS else 18
        amount = (int(amount * (10 ** decimals)))

        path_id = await self.get_path_id(chain_id, token_from_address, token_to_address, amount, my_address)

        if token_from_address != ETH_ADDRESS:
            await self.approve_token(client, token_contract, router_contract_address, amount)

        quote = await self.get_swap_data(my_address, path_id)

        transaction = quote['transaction']

        await client.transactions.send(
            contract_address=transaction["to"],
            encoded_data=transaction["data"],
            tx_value=transaction["value"],
        )

        return {
            'network': self._params.network.name,
            'from': token_from.symbol,
            'to': token_to.symbol,
            'amount': amount,
        }


    async def get_path_id(self, chain_id, token_from_address, token_to_address, amount, my_address):
        input_tokens = [
            {
                "tokenAddress": token_from_address,
                "amount": str(amount)
            }
        ]
        output_tokens = [
            {
                "tokenAddress": token_to_address,
                "proportion": 1.0
            }
        ]
        payload = {
            "chainId": chain_id,
            "inputTokens": input_tokens,
            "outputTokens": output_tokens,
            "userAddr": my_address,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post('https://api.odos.xyz/sor/quote/v2', json=payload, proxy=self._client.w3.proxy) as response:
                data = await response.json()
                return data["pathId"]


    async def get_swap_data(self, my_address, path_id):
        url = "https://api.odos.xyz/sor/assemble"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        payload = {
            "userAddr": my_address,
            "pathId": path_id,
            "simulate": True
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers, proxy=self._client.w3.proxy) as response:
                return await response.json()


    async def approve_token(self, client, token_contract, spender, amount):
        owner = client.wallet.public_key
        current_allowance = await token_contract.functions.allowance(owner, spender).call()
        logger.info(f"Allowance: {current_allowance}")

        if current_allowance >= amount:
            return

        encoded_data = token_contract.encode_abi(
            'approve',
            args=[spender, amount]
        )

        await client.transactions.send(
            contract_address=token_contract.address,
            encoded_data=encoded_data,
        )