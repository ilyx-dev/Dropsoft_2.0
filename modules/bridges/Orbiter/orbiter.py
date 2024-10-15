import logging

from models.interfaces.ibridge import IBridge

logger = logging.getLogger(__name__)

class Orbiter(IBridge):
    async def bridge(self) -> dict:
        logger.info('Bridge successful')
        return {
            'from': "ETH",
            'to': "USDT"
        }