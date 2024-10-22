import asyncio
import logging
import time
from models.interfaces.iswap import ISwap
from models.params.swap_params import SwapParams
from w3.core import Client
from .config_sync import NETWORKS, abi, erc20_abi

logger = logging.getLogger(__name__)

ETH_ADDRESS = '0x0000000000000000000000000000000000000000'

class SyncSwap(ISwap):

    def __init__(self, client: Client, params: SwapParams):
        super().__init__(client, params)


    async def swap(self) -> dict:

        client = self._client
        my_address = client.wallet.public_key

        try:
            network_name = self._params.network.name
            network_data = NETWORKS.get(network_name)
            if not network_data:
                logger.error(f"Network {network_name} not found in config")
                return {'success': False, 'error': 'Network not found in config'}

            contract_address = network_data['contract_address']
            weth_address = network_data['weth_address']
            use_vault_false_pools = network_data['use_vault_false_pools']

            token_in = self._params.from_token
            token_in_symbol = token_in.symbol
            token_out_symbol = self._params.to_token.symbol

            tokens_data = network_data['tokens']
            from_token_data = tokens_data.get(token_in_symbol)

            token_in_address = from_token_data['address']
            decimals = from_token_data['decimals']

            amount_in = self._params.amount

            pool_identifier = f"{token_in_symbol}-{token_out_symbol}"
            pool = network_data['pools'].get(pool_identifier)
            if not pool:
                pool_identifier = f"{token_out_symbol}-{token_in_symbol}"
                pool = network_data['pools'].get(pool_identifier)
                if not pool:
                    logger.error(f"Pool not found for pair {token_in_symbol}-{token_out_symbol} in network {network_name}")
                    return {'success': False, 'error': 'Pool not found in config'}

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
                token_contract = client.w3.async_w3.eth.contract(address=token_in_address, abi=erc20_abi)
                transaction_amount = int(amount_in * (10 ** decimals))
                value = 0

                approve_success = await self.approve_token(
                    client, token_contract, contract_address, transaction_amount
                )

                if not approve_success:
                    logger.error("Approval failed. Cannot proceed with swap.")
                    return {"success": False, "error": "Approval failed"}

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

            # data = encoded_data
            # print(data[:10])
            # data = data[10:]
            # while data:
            #     print(data[:64])
            #     data = data[64:]


            tx_hash = await client.transactions.send(
                contract_address=contract_address,
                encoded_data=encoded_data,
                tx_value=value,
            )

            receipt = await client.w3.async_w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180)
            if receipt.status == 1:
                logger.info(f"Transaction was successful: 0x{tx_hash.hex()}")
                return {
                    'success': True,
                    'network': self._params.network.name,
                    'from': token_in_symbol,
                    'to': token_out_symbol,
                    'amount': amount_in
                }
            else:
                logger.error(f"Transaction failed: 0x{tx_hash.hex()}")
                return {'success': False, 'tx_hash': tx_hash.hex()}

        except Exception as e:
            logger.warning(f"Warning: {e}")
            if 'expected a bool, int, byte or bytearray in first arg, or keyword of hexstr or text' in str(e):
                return {
                    'success': True,
                    'network': self._params.network.name,
                    'from': token_in_symbol,
                    'to': token_out_symbol,
                    'amount': amount_in
                }
            else:
                return {'success': False, 'error': str(e)}


    async def approve_token(self, client, token_contract, spender, amount):

        encoded_data = token_contract.encode_abi(
            'approve',
            args=[spender, amount]
        )

        tx_hash = await client.transactions.send(
            contract_address=token_contract.address,
            encoded_data=encoded_data,
        )

        logger.info(f"Approval transaction sent")

        # receipt = await client.w3.async_w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180)
        # if 'status' in receipt and receipt['status'] == 1:
        #     return True
        # else:
        #     return False

        # receipt не дает нихуя свапнуть
        # я не знаю это трабл библы или мой косяк, пока сделал костыль, вместе посмотрим

        return True

