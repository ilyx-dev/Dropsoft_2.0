import logging

from models.interfaces.ibridge import IBridge

logger = logging.getLogger(__name__)

class Owlto(IBridge):
    async def bridge(self) -> dict:
        logger.info('Bridge successful')

        return {
            'token': self._params.token.symbol,
            'from_network': "",
            'to_network': "",
            'amount': ""
        }