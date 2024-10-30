from abc import ABC, abstractmethod

from validators.params_validator import ParamsValidator


class IParams(ABC):
    """
    Интерфейс для классов параметров, используемых в модулях.
    Разработчики модулей должны наследоваться от этого класса при создании параметров для своих модулей.
    """

    @abstractmethod
    def __init__(self, params: dict, validator: ParamsValidator):
        """
        Общая инициализация для всех классов параметров.
        """
        pass

    @abstractmethod
    def validate_selection_params(self, supported_chains: dict) -> None:
        """
        Валидирует параметры, необходимые для выбора модуля (например, сети, токены).
        Должен выбрасывать исключение, если валидация не пройдена.
        """
        pass

    @abstractmethod
    async def validate_amount_params(self, client) -> None:
        """
        Асинхронно валидирует и обрабатывает параметры, связанные с количеством.
        Должен выбрасывать исключение, если валидация не пройдена.
        """
        pass

    @abstractmethod
    def get_chain(self):
        """
        Возвращает сеть или цепочку, связанную с этими параметрами.

        Returns:
            Объект сети или цепочки.
        """
        pass
