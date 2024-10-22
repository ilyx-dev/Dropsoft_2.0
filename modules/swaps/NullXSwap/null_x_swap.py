import logging

from models.interfaces.iswap import ISwap

logger = logging.getLogger(__name__)

class NullXSwap(ISwap):
    async def swap(self) -> dict:
        logger.info('Swap successful')

        return {
            'network': "",
            'from': "",
            'to': "",
            'amount': ""
        }