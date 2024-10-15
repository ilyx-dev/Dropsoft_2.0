import logging
from abc import abstractmethod

from w3.core import Client

from models.interfaces.imodule import IModule
from models.params.swap_params import SwapParams

logger = logging.getLogger(__name__)

class ISwap(IModule[SwapParams]):

    def __init__(self, client: Client, params: SwapParams):
        super().__init__(client, params)
        self._pre_swap_balance = None

    async def execute(self) -> dict:
        self._pre_swap_balance = await self._client.wallet.get_balance(self._params.to_token.address)
        logger.debug(f"Pre-swap balance of {self._params.to_token.symbol}: {self._pre_swap_balance.get_converted_amount()}")

        swap_result = await self.swap()
        return swap_result

    @abstractmethod
    async def swap(self) -> dict:
        """Метод, для свапа, который будет реализован в наследниках."""
        pass

    async def verify(self) -> bool:
        post_swap_balance = await self._client.wallet.get_balance(self._params.to_token.address)
        post_swap_amount = post_swap_balance.get_converted_amount()
        logger.debug(f"Post-swap balance of {self._params.to_token.symbol}: {post_swap_amount}")

        balance_difference = post_swap_amount - self._pre_swap_balance.get_converted_amount()

        if balance_difference > 0:
            logger.info(f"Swap verified successfully. Balance difference: {balance_difference}")
            return True
        else:
            logger.info(f"Swap verification failed. Balance difference: {balance_difference}")
            return False