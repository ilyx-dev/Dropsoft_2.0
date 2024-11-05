import logging
import time

import w3.utils

from models.interfaces.iswap import ISwap
from models.params.swap_params import SwapParams
from w3.core import Client
from .config_sync import NETWORKS, abi

logger = logging.getLogger(__name__)

ETH_ADDRESS = '0x0000000000000000000000000000000000000000'

class SyncSwap(ISwap):

    def __init__(self, client: Client, params: SwapParams):
        super().__init__(client, params)


    async def swap(self) -> dict:
        client = self._client
        my_address = client.wallet.public_key

        network_name = self._params.network.name
        network_data = NETWORKS.get(network_name)

        contract_address = network_data['contract_address']
        weth_address = self._params.network.get_token_by_symbol("WETH").address

        use_vault_false_pools = network_data['use_vault_false_pools']

        token_in = self._params.from_token
        token_out = self._params.to_token

        token_in_symbol = token_in.symbol
        token_out_symbol = token_out.symbol

        if token_in.address:
            token_in_address = w3.utils.to_checksum_address(token_in.address)
            erc20_contract = client.contracts.get_erc20_contract(token_in_address)
            decimals = await erc20_contract.functions.decimals().call()
        else:
            token_in_address = ETH_ADDRESS

        amount_in = self._params.amount

        pool_identifier = f"{token_in_symbol}-{token_out_symbol}"
        pool = network_data['pools'].get(pool_identifier)

        if not pool:
            pool_identifier = f"{token_out_symbol}-{token_in_symbol}"
            pool = network_data['pools'].get(pool_identifier)
            if not pool:
                error_message = f"Pool not found {pool_identifier}"
                raise ValueError(error_message)

        amount_out_min = 0

        sync_swap_router_contract = client.contracts.get_contract(
            contract_address=contract_address,
            abi=abi
        )

        is_eth_in = token_in_address.lower() == ETH_ADDRESS.lower()

        use_vault_flag = True
        if pool.lower() in [p.lower() for p in use_vault_false_pools]:
            use_vault_flag = False

        if is_eth_in:
            transaction_amount = int(amount_in * 1e18)
            value = transaction_amount
            token_in_data_address = weth_address

        else:
            token_contract = self._client.contracts.get_erc20_contract(token_in_address)
            transaction_amount = int(amount_in * (10 ** decimals))
            value = 0
            await self.approve_token(client, token_contract, contract_address, transaction_amount)

            token_in_data_address = token_in_address

        flag = "2" if token_in_address.lower() == ETH_ADDRESS.lower() else "1"

        paths = [
            {
                'steps': [
                    {
                        'pool': pool,
                        'data': f"0x{token_in_data_address[2:].zfill(64)}"
                                f"{my_address[2:].zfill(64)}"
                                f"{flag.zfill(64)}",
                        'callback': "0x0000000000000000000000000000000000000000",
                        'callbackData': "0x",
                        'useVault': use_vault_flag
                    }
                ],
                'tokenIn': token_in_address,
                'amountIn': transaction_amount
            }
        ]

        deadline = int(time.time()) + 60 * 20

        encoded_data = sync_swap_router_contract.encode_abi(
            'swap',
            args=[paths, amount_out_min, deadline]
        )

        await client.transactions.send(
            contract_address=contract_address,
            encoded_data=encoded_data,
            tx_value=value,
        )

        logger.info(f"Swap successful: {self._params.amount} {self._params.from_token.symbol} to {self._params.to_token.symbol} in {self._params.network.name}")

        return {
            'network': self._params.network.name,
            'from': token_in_symbol,
            'to': token_out_symbol,
            'amount': amount_in
        }


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


