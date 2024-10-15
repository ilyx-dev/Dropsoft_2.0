from utils.helpers import read_json_file


class ConfigManager:
    def __init__(self, config_path: str):
        self._config = read_json_file(config_path)

    def get_config(self):
        return self._config

    def _get_specific_config(self, keys):
        return {key: self._config.get(key) for key in keys}

    def get_wallet_processor_config(self):
        wallet_processor_keys = [
            'THREADS', 'RETRY', 'USE_SCENARIOS', 'SCENARIO',
            'SLEEP_BETWEEN_MODULES', 'WALLET_RANDOMIZER',
            'MAX_GWEI', 'MAX_GAS_CHARGE', 'CHECK_GWEI',
            'SLEEP_BETWEEN_GWEI_CHECKS', 'MODULES'
        ]
        return self._get_specific_config(wallet_processor_keys)

    def get_proxy_manager_config(self):
        proxy_manager_keys = ['RPCS_FOR_PROXY']
        return self._get_specific_config(proxy_manager_keys)