import logging
import aiohttp
import w3.utils

from models.interfaces.iswap import ISwap
from .config_symbiosis import *

logger = logging.getLogger(__name__)


class SymbiosisSwap(ISwap):

    async def swap(self) -> dict:
        client = self._client
        token_in = self._params.from_token
        token_out = self._params.to_token
        amount = self._params.amount

        token_in_address = w3.utils.to_checksum_address(token_in.address if token_in.address else ETH_ADDRESS)
        token_out_address = w3.utils.to_checksum_address(token_out.address if token_out.address else ETH_ADDRESS)
        token_out_symbol = self._params.to_token.symbol

        my_address = w3.utils.to_checksum_address(client.wallet.public_key)
        token_contract_in = self._client.contracts.get_erc20_contract(token_in_address)
        erc20_contract_one = client.contracts.get_erc20_contract(token_in_address)
        erc20_contract_two = client.contracts.get_erc20_contract(token_out_address)
        decimals_one = await erc20_contract_one.functions.decimals().call() if token_in_address != ETH_ADDRESS else 18
        decimals_two = await erc20_contract_two.functions.decimals().call() if token_out_address != ETH_ADDRESS else 18

        total_amount = int(amount * 10 ** decimals_one)
        chain_id = self._params.network.chain_id
        slippage = 5

        logger.info(f'API STATUS: {await self.check_api()}')
        quote = await self.get_quote(token_in_address, token_out_address, str(total_amount), chain_id, decimals_one, decimals_two, my_address, my_address, slippage, token_out_symbol)
        transaction = quote['tx']
        spender = w3.utils.to_checksum_address(transaction['to'])

        if token_in_address != ETH_ADDRESS:
            await self.approve_token(client, token_contract_in, spender, total_amount)

        await client.transactions.send(
            contract_address=w3.utils.to_checksum_address(transaction['to']),
            encoded_data=transaction['data'],
            tx_value=transaction['value'],
        )

        return {
            'network': self._params.network.name,
            'from': token_in.symbol,
            'to': token_out.symbol,
            'amount': amount,
        }

    async def check_api(self):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.symbiosis.finance/crosschain/health-check") as resp:
                return await resp.text()


    async def get_quote(self, token_in_address, token_out_address, amount, chain_id, decimals_one, decimals_two, from_address, to_address, slippage, symbol):
        payload = {
            "tokenAmountIn": {
                "address": token_in_address,
                "amount": amount,
                "chainId": chain_id,
                "decimals": decimals_one
            },
            "tokenOut": {
                "chainId": chain_id,
                "address": token_out_address,
                "symbol": symbol,
                "decimals": decimals_two
            },
            "from": from_address,
            "to": to_address,
            "slippage": slippage
        }

        async with aiohttp.ClientSession() as session:
            async with session.post('https://api.symbiosis.finance/crosschain/v1/swap', json=payload) as resp:
                return await resp.json()

    async def approve_token(self, client, token_contract, spender, approve_amount):
        owner = client.wallet.public_key
        current_allowance = await token_contract.functions.allowance(owner, spender).call()
        logger.info(f"Allowance: {current_allowance}")

        if current_allowance >= approve_amount:
            return

        encoded_data = token_contract.encode_abi(
            'approve',
            args=[spender, approve_amount]
        )

        await client.transactions.send(
            contract_address=token_contract.address,
            encoded_data=encoded_data,
        )