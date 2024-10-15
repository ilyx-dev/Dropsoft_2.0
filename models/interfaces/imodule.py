import logging
from abc import abstractmethod, ABC
from typing import TypeVar, Generic

from w3.core import Client

from models.interfaces.iparams import IParams

logger = logging.getLogger(__name__)

ParamsType = TypeVar('ParamsType', bound=IParams)

class IModule(ABC, Generic[ParamsType]):

    def __init__(self, client: Client, params: ParamsType):
        self._client = client
        self._params = params

    @abstractmethod
    async def execute(self) -> dict:
        """Основной метод выполнения модуля."""
        pass

    @abstractmethod
    async def verify(self) -> bool:
        """Метод для верификации выполнения модуля."""
        pass

    def __repr__(self):
        return f"<IModule(params={self._params})>"