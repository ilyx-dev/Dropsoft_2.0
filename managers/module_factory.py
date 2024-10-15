from w3.core import Client

from configs.params_registry import module_type_to_params_class
from models.interfaces.imodule import IModule
from models.interfaces.iparams import IParams


class ModuleFactory:
    def __init__(self, modules_registry):
        self._modules_registry = modules_registry

    def get_module(self, module_name: str, client: Client, params: IParams) -> IModule:
        module_entry = self._get_module_entry(module_name)
        module_class = module_entry['class']

        module_instance = module_class(client, params)
        return module_instance


    def _get_module_entry(self, module_name):
        module_entry = self._modules_registry.get(module_name)
        if not module_entry:
            raise ValueError(f"Module '{module_name}' not found in registry")
        return module_entry

    def get_module_type(self, module_name: str) -> str:
        module_entry = self._modules_registry.get(module_name)
        if not module_entry:
            raise ValueError(f"Module {module_name} not found in registry")
        return module_entry['type'].value

    def get_all_module_names(self) -> list:
        return list(self._modules_registry.keys())
