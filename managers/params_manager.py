from w3.core import Client

from configs.params_registry import module_type_to_params_class
from models.interfaces.iparams import IParams
from validators.params_validator import ParamsValidator


class ParamsManager:
    """
    Класс для валидации параметров модулей на основе информации из module_registry.
    """

    def __init__(self, module_name: str, modules_registry: dict, params: dict):
        self.module_name = module_name
        self._module_entry = modules_registry.get(module_name)
        if not self._module_entry:
            raise ValueError(f"Module '{module_name}' is not found in the registry.")

        self.supported_chains = self._module_entry.get('supported_chains')
        self.module_type = self._module_entry['type']

        # First, try to get the params_class from the module entry
        params_class = self._module_entry.get('params_class')
        if not params_class:
            # Fallback to module_type_to_params_class mapping
            params_class = module_type_to_params_class.get(self.module_type)
            if not params_class:
                raise ValueError(f"No parameter class for module type '{self.module_type.value}'.")

        validator = ParamsValidator(module_name, modules_registry)
        self._params = params_class(params, validator)

    def validate_selection_params(self) -> None:
        """
        Валидирует параметры, необходимые для выбора модуля.
        """
        self._params.validate_selection_params(self.supported_chains)

    async def validate_amount_params(self, client: Client) -> None:
        """
        Валидирует и преобразует параметры, необходимые для запуска модуля (amount, min_amount).
        """
        await self._params.validate_amount_params(client)

    def get_params(self) -> IParams:
        """
        Возвращает экземпляр параметров для использования в модуле.
        """
        return self._params

