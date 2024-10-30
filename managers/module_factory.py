from w3.core import Client

from adapters.network_adapter import convert_to_web3_network
from managers.module_selector import ModuleSelector
from managers.params_manager import ParamsManager
from models.enums.module_type import ModuleType
from models.interfaces.imodule import IModule


class ModuleFactory:
    def __init__(self, modules_registry: dict, module_selector: ModuleSelector):
        self._modules_registry = modules_registry
        self._module_selector = module_selector

    async def create_module_instance(
        self,
        module_name_or_type: str,
        params: dict,
        private_key: str,
        proxy: str
    ) -> IModule:
        module_name, module_class = self._module_selector.select_module(module_name_or_type, params)

        params_manager = ParamsManager(module_name, self._modules_registry, params)
        params_manager.validate_selection_params()

        network = params_manager.get_params().get_chain()

        client = await Client(private_key, convert_to_web3_network(network), proxy)

        await params_manager.validate_amount_params(client)

        module_params = params_manager.get_params()

        module_instance = module_class(client, module_params)

        return module_instance

    def determine_module_type(self, module_name_or_type: str) -> ModuleType:
        if module_name_or_type in self._modules_registry:
            module_entry = self._modules_registry[module_name_or_type]
            return module_entry['type']
        else:
            try:
                return ModuleType(module_name_or_type.lower())
            except ValueError:
                raise ValueError(f"Unknown module type or module name '{module_name_or_type}'")

    def get_all_module_names(self) -> list:
        return list(self._modules_registry.keys())
