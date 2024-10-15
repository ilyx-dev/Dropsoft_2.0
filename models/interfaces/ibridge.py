import logging
from abc import abstractmethod

from w3.core import Client

from adapters.network_adapter import convert_to_web3_network
from models.interfaces.imodule import IModule
from models.params.bridge_params import BridgeParams

logger = logging.getLogger(__name__)

class IBridge(IModule[BridgeParams]):

    def __init__(self, client: Client, params: BridgeParams):
        super().__init__(client, params)
        self._to_network_client = None
        self._pre_bridge_balance = None

    async def execute(self) -> dict:
        self._to_network_client = await self._client.switch_network(convert_to_web3_network(self._params.to_network))
        self._pre_bridge_balance = await self._to_network_client.wallet.get_balance(self._params.token.address)
        logger.debug(f"Pre-bridge balance of {self._params.token.symbol} on {self._params.to_network.name}: {self._pre_bridge_balance.get_converted_amount()}")

        bridge_result = await self.bridge()
        return bridge_result

    @abstractmethod
    async def bridge(self) -> dict:
        """Метод, для бриджа, который будет реализован в наследниках."""
        pass

    async def verify(self) -> bool:
        post_bridge_balance = await self._to_network_client.wallet.get_balance(self._params.token.address)
        post_bridge_amount = post_bridge_balance.get_converted_amount()
        logger.debug(f"Post-bridge balance of {self._params.token.symbol} on {self._params.to_network.name}: {post_bridge_amount}")

        balance_difference = post_bridge_amount - self._pre_bridge_balance.get_converted_amount()

        if balance_difference > 0:
            logger.info(f"Bridge verified successfully. Balance difference: {balance_difference}")
            return True
        else:
            logger.info(f"Bridge verification failed. Balance difference: {balance_difference}")
            return False