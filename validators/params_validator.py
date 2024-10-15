from configs.networks import Networks
from configs.params_registry import module_type_to_params_class
from models.interfaces.iparams import IParams
from models.network import Network
from models.token import Token

class ParamsValidator:
    """
    Класс ParamsValidator предназначен для валидации параметров модулей на основе информации из module_registry.
    Он обеспечивает проверку поддерживаемых сетей и токенов для конкретного модуля.

    Attributes:
        _module_entry (dict): Входная запись конкретного модуля из реестра, содержащая информацию о поддерживаемых сетях и токенах.
        supported_chains (dict): Словарь поддерживаемых сетей и токенов в них для текущего модуля.
    """

    def __init__(self, module_name: str, modules_registry: dict):
        self._module_entry = modules_registry.get(module_name)
        if not self._module_entry:
            raise ValueError(f"Module {module_name} is not found in the registry.")
        self.supported_chains = self._module_entry['supported_chains']

    def validate_network(self, network_name: str) -> Network:
        """
        Валидирует сеть для текущего модуля и возвращает ее.

        Args:
            network_name (str): Название сети, которую нужно проверить.

        Returns:
            Network: Объект Network для переданной сети, если она поддерживается модулем.

        Raises:
            ValueError: Если указанная сеть не поддерживается модулем.
        """
        if network_name.lower() not in [chain.lower() for chain in self.supported_chains.keys()]:
            raise ValueError(
                f"Network {network_name} is not supported by module {self._module_entry['class'].__name__}"
            )
        return Networks.from_str(network_name)

    def validate_token(self, network: Network, token_symbol: str) -> Token:
        """
        Валидирует токен для указанной сети и возвращает его.

        Args:
            network (Network): Объект сети, в которой проводится проверка.
            token_symbol (str): Символ токена, который нужно проверить.

        Returns:
            Token: Объект Token для переданного символа токена, если он поддерживается в указанной сети.

        Raises:
            ValueError: Если указанный токен не поддерживается для данной сети.
        """
        supported_tokens = [token.lower() for token in self.supported_chains[network.name]]
        token_symbol = token_symbol.lower()

        if token_symbol not in supported_tokens:
            raise ValueError(
                f"Token {token_symbol} is not supported on network {network.name}"
            )

        return network.get_token_by_symbol(token_symbol)


    async def get_params(self, params_data, private_key: str, proxy: str) -> IParams:
        module_type = self._module_entry['type']

        params_class = module_type_to_params_class.get(module_type)
        if not params_class:
            raise ValueError(f"No parameter class for '{module_type.name}' type")

        return await params_class(params_data, self, private_key, proxy)
