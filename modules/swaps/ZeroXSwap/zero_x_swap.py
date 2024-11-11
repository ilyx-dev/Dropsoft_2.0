import logging
import aiohttp
import w3.utils

from eth_account import Account
from w3.core import Client
from models.params.swap_params import SwapParams
from models.interfaces.iswap import ISwap
from .config_zerox import *

logger = logging.getLogger(__name__)


class ZeroXSwap(ISwap):

    def __init__(self, client: Client, params: SwapParams):
        super().__init__(client, params)

    async def swap(self) -> dict:

        client = self._client
        token_in = self._params.from_token
        token_out = self._params.to_token
        amount = self._params.amount

        token_in_address = w3.utils.to_checksum_address(token_in.address if token_in.address else NATIVE_ADDRESS)
        token_out_address = w3.utils.to_checksum_address(token_out.address if token_out.address else NATIVE_ADDRESS)

        erc20_contract = client.contracts.get_erc20_contract(token_in_address)
        decimals = await erc20_contract.functions.decimals().call() if token_in_address != NATIVE_ADDRESS else 18
        sell_amount = int(amount * (10 ** decimals))

        my_address = w3.utils.to_checksum_address(client.wallet.public_key)
        token_contract = self._client.contracts.get_erc20_contract(token_in_address)
        spender = w3.utils.to_checksum_address(ZEROX_PERMIT2_ADDRESS)

        if token_in_address != NATIVE_ADDRESS:
            await self.approve_token(client, token_contract, spender, sell_amount)

        quote = await self.fetch_quote(sell_amount, token_in_address, token_out_address, my_address)
        transaction = quote['transaction']
        transaction['to'] = w3.utils.to_checksum_address(transaction['to'])

        if quote.get('permit2') and 'eip712' in quote['permit2']:
            permit_signature = await self.sign_permit2(quote['permit2']['eip712'])
            signature_length = len(permit_signature) // 2
            signature_length_hex = client.w3.async_w3.to_hex(signature_length)[2:].zfill(64)
            transaction['data'] += signature_length_hex + permit_signature

        await client.transactions.send(
            contract_address=transaction['to'],
            encoded_data=transaction['data'],
            tx_value=transaction['value'],
        )

        return {
            'network': self._params.network.name,
            'from': token_in.symbol,
            'to': token_out.symbol,
            'amount': sell_amount,
        }


    async def fetch_quote(self, sell_amount, token_in, token_out, my_address):
        params = {
            'chainId': self._params.network.chain_id,
            'sellToken': token_in,
            'buyToken': token_out,
            'sellAmount': str(sell_amount),
            'taker': my_address
        }
        headers = {
            'Content-Type': 'application/json',
            '0x-api-key': ZEROX_API_KEY,
            '0x-version': 'v2'
        }
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.0x.org/swap/permit2/quote', params=params, headers=headers, proxy=self._client.w3.proxy) as response:
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


    async def sign_permit2(self, eip712_message):
        signed_message = Account.sign_typed_data(self._client.wallet.private_key, full_message=eip712_message)
        return signed_message.signature.hex()
