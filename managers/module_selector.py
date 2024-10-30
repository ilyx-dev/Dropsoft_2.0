import random

from managers.params_manager import ParamsManager
from models.enums.module_type import ModuleType


class ModuleSelector:
    def __init__(self, modules_registry):
        self._modules_registry = modules_registry

    def select_module(self, module_name_or_type: str, params: dict):
        if module_name_or_type in self._modules_registry:
            # Конкретный модуль указан
            module_entry = self._modules_registry[module_name_or_type]
            return module_name_or_type, module_entry['class']
        else:
            # Указан тип модуля (например, 'swap' или 'bridge')
            module_type = ModuleType(module_name_or_type.lower())
            compatible_modules = self._find_compatible_modules(module_type, params)
            if not compatible_modules:
                raise ValueError(f"No compatible modules found for type '{module_type.value}' with given parameters.")
            selected_module_name = random.choice(compatible_modules)
            module_entry = self._modules_registry[selected_module_name]
            return selected_module_name, module_entry['class']

    def _find_compatible_modules(self, module_type: ModuleType, params: dict):
        compatible_modules = []
        for module_name, module_info in self._modules_registry.items():
            if module_info['type'] == module_type:
                manager = ParamsManager(module_name, self._modules_registry, params)
                try:
                    # Проверяем, подходят ли параметры для этого модуля
                    manager.validate_selection_params()
                    compatible_modules.append(module_name)
                except ValueError:
                    # Параметры не подходят для данного модуля
                    continue
        return compatible_modules


