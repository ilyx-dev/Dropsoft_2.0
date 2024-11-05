import logging
import aiohttp
import w3.utils

from models.interfaces.iswap import ISwap
from .config_open_ocean import *

logger = logging.getLogger(__name__)


class OpenOceanSwap(ISwap):

    async def swap(self) -> dict:
        client = self._client
        token_in = self._params.from_token
        token_out = self._params.to_token
        amount = self._params.amount

        token_in_address = w3.utils.to_checksum_address(token_in.address if token_in.address else ETH_ADDRESS)
        token_out_address = w3.utils.to_checksum_address(token_out.address if token_out.address else ETH_ADDRESS)

        my_address = w3.utils.to_checksum_address(client.wallet.public_key)
        token_contract = self._client.contracts.get_erc20_contract(token_in_address)

        if self._params.network.name != 'zksync':
            spender = w3.utils.to_checksum_address(contract_address)
        else:
            spender = w3.utils.to_checksum_address(zk_contract_address)

        if token_in_address != ETH_ADDRESS:
            await self.approve_token(client, token_contract, spender, amount)

        chain = self._params.network.name.lower()
        slippage = 1

        gas_price = await client.w3.async_w3.eth.gas_price
        quote = await self.get_quote(token_in_address, token_out_address, amount, slippage, str(gas_price), my_address, chain)
        transaction = quote['data']

        await client.transactions.send(
            contract_address= w3.utils.to_checksum_address(transaction['to']),
            encoded_data=transaction['data'],
            tx_value=transaction['value'],
        )

        return {
            'network': self._params.network.name,
            'from': token_in.symbol,
            'to': token_out.symbol,
            'amount': amount,
        }

    async def get_quote(self, token_in_address, token_out_address, amount, slippage, gas_price, my_address, chain):
        params = {
            'chain': chain,
            'inTokenAddress': token_in_address,
            'outTokenAddress': token_out_address,
            'amount': amount,
            'slippage': slippage,
            'gasPrice': gas_price,
            'account': my_address
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://open-api.openocean.finance/v3/{chain}/swap_quote', params=params) as response:
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