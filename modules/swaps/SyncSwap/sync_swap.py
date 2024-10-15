import logging

from models.interfaces.iswap import ISwap

logger = logging.getLogger(__name__)

class SyncSwap(ISwap):
    async def swap(self) -> dict:
        logger.info('Swap successful')

        contract = self._client.w3.async_w3.eth.contract()

        encoded_data = contract.encodeABI(
            fn_name='transfer',
            args=[
                '0xRecipientAddressHere',
                1000
            ]
        )

        await self._client.transactions.send(contract, encoded_data, 0)

        return {
            'from': "ETH",
            'to': "USDT"
        }