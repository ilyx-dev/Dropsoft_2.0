import asyncio
import logging
import aiohttp
from decimal import Decimal

import w3.utils
from w3.utils.exceptions import GasEstimationFailedException

from models.interfaces.ibridge import IBridge
from w3.core.client import Client

from modules.bridges.Stargate.config import STARGATE_CONTRACTS, STARGATE_POOLS_ID, STARGATE_ABI, LAYERZERO_CHAINS_ID

logger = logging.getLogger(__name__)
ZERO_ADDRESS = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'
# При выполнение бриджа натив токена amount = получить в замен, а комса платится сверху
class Stargate(IBridge):

    async def bridge(self) -> dict:
        from_chain = self._params.from_network.name
        to_chain = self._params.to_network.name
        wallet = self._client.wallet.public_key

        token_in = self._params.token.address or ZERO_ADDRESS

        if token_in == ZERO_ADDRESS:
            decimals = 18
        else:
            token_contract = self._client.contracts.get_erc20_contract(w3.utils.to_checksum_address(token_in))
            decimals = await token_contract.functions.decimals().call()

        amount = int(self._params.amount * (10 ** decimals))

        dst_chain_id = LAYERZERO_CHAINS_ID[to_chain]
        min_amount_out = int(amount * 0.995)

        router_contract_address = w3.utils.to_checksum_address(STARGATE_CONTRACTS[from_chain]['router'])
        router_contract = self._client.contracts.get_contract(STARGATE_ABI['router'], router_contract_address)

        function_type = 1
        dst_gas_for_call = 0
        dst_native_amount = 0
        dst_native_addr = '0x0000000000000000000000000000000000000001'
        to_token_symbol = self._params.token.symbol

        estimate_fee = (await router_contract.functions.quoteLayerZeroFee(
            dst_chain_id, function_type,
            w3.utils.to_checksum_address(STARGATE_CONTRACTS[to_chain][to_token_symbol]),
            '0x',
            (dst_gas_for_call, dst_native_amount, dst_native_addr)
        ).call())[0]

        balance = await self._client.wallet.get_balance(self._params.token.address)
        balance = balance.get_converted_amount()

        if balance <= estimate_fee/10**18:
            print(1)
            logger.error('Not enough to pay for gas')
            raise GasEstimationFailedException

        if token_in == ZERO_ADDRESS:
            if balance <= (estimate_fee/10**18 + self._params.amount):
                logger.error('Not enough to pay for gas')
                raise GasEstimationFailedException
            router_contract_address = w3.utils.to_checksum_address(STARGATE_CONTRACTS[from_chain]['router_eth'])
            router_contract = self._client.contracts.get_contract(STARGATE_ABI['router_eth'], router_contract_address)
            tx_data = router_contract.encode_abi(
                'swapETH',
                args=(dst_chain_id, wallet, wallet, amount, min_amount_out)
            )
            await self._client.transactions.send(
                encoded_data=tx_data,
                contract_address=router_contract_address,
                tx_value=amount + estimate_fee
            )
        else:
            scr_pool_id = STARGATE_POOLS_ID[from_chain][self._params.token.symbol] or None
            dst_pool_id = STARGATE_POOLS_ID[to_chain][self._params.token.symbol] or None

            tx_data = router_contract.encode_abi(
                'swap',
                args=(dst_chain_id, scr_pool_id, dst_pool_id, wallet, amount, min_amount_out,
                      [dst_gas_for_call, dst_native_amount, dst_native_addr], wallet, '0x')
            )
            token_contract = self._client.contracts.get_erc20_contract(self._params.token.address)
            await self._approve_token(self._client, token_contract, router_contract_address, amount)

            await self._client.transactions.send(
                encoded_data=tx_data,
                contract_address=router_contract_address,
                tx_value=estimate_fee
            )

        logger.info(f"Bridge successful: {self._params.amount} {self._params.token.symbol} from {from_chain} to {to_chain}")

        return {
            'token': self._params.token.symbol,
            'from_network': from_chain,
            'to_network': to_chain,
            'amount': self._params.amount
        }

    async def _approve_token(self, client, token_contract, spender, amount):
        owner = client.wallet.public_key
        current_allowance = await token_contract.functions.allowance(owner, spender).call()
        decimals = await token_contract.functions.decimals().call()
        logger.info(f"Current allowance: {current_allowance / 10 ** decimals}")

        if current_allowance < amount:
            logger.info("Executing approve transaction.")
            encoded_data = token_contract.encode_abi(
                'approve',
                args=[spender, amount]
            )
            await client.transactions.send(
                encoded_data=encoded_data,
                contract_address=token_contract.address
            )
            logger.info(f"Approved token: {token_contract.address}")
        else:
            logger.info("Allowance is sufficient, no need to approve.")
