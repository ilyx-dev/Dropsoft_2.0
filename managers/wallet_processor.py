import asyncio
import logging
import random

from w3.core.client import Client

from adapters.network_adapter import convert_to_web3_network
from managers.module_factory import ModuleFactory
from managers.proxy_manager import ProxyManager
from managers.scenario_manager import ScenarioManager
from utils.contextvar import wallet_address_var
from utils.helpers import get_wallet_address_from_private_key, wait_gwei
from validators.params_validator import ParamsValidator

logger = logging.getLogger(__name__)

class WalletProcessor:
    def __init__(self, private_keys: list[str], recipients: list[str], proxy_manager: ProxyManager, scenario_manager: ScenarioManager, module_factory: ModuleFactory, modules_registry: dict, config: dict):
        self._private_keys = private_keys
        self._recipients = recipients
        self._proxy_manager = proxy_manager
        self._scenario_manager = scenario_manager
        self._module_factory = module_factory
        self._modules_registry = modules_registry
        self._config = config
        self._wallet_histories = {}
        self._semaphore = asyncio.Semaphore(self._config['THREADS'])  # THREADS

    async def process_wallets(self):
        if self._config['WALLET_RANDOMIZER']:
            random.shuffle(self._private_keys)  # WALLET_RANDOMIZER

        if self._config['USE_SCENARIOS']:
            input('Press ENTER to start SCENARIO')
            tasks = [self._limited_process(self._process_wallet_via_scenario, private_key) for private_key in self._private_keys]
        else:
            module_names = self._module_factory.get_all_module_names()
            print("Select Module:")
            for index, name in enumerate(module_names, start=1):
                print(f"{index}. {name}")
            selected_index = int(input("Enter the number of the module you want to select: ")) - 1
            selected_module = module_names[selected_index]
            tasks = [self._limited_process(self._process_wallet_via_module, private_key, selected_module) for private_key in self._private_keys]
        await asyncio.gather(*tasks)
        print(self._wallet_histories)

    async def _limited_process(self, func, *args, **kwargs):
        async with self._semaphore:
            await func(*args, **kwargs)

    async def _process_wallet_via_scenario(self, private_key: str):
        wallet_address = get_wallet_address_from_private_key(private_key)

        wallet_address_var.set(wallet_address)
        proxy = await self._proxy_manager.get_random_proxy()
        self._wallet_histories[wallet_address] = []

        scenario_name = self._config['SCENARIO']
        scenario = self._scenario_manager.get_scenario(scenario_name)
        scenario_type = scenario['type']

        modules = scenario['module_sequence'] if scenario_type == 'STRICT' else random.sample(
            scenario['module_sequence'], len(scenario['module_sequence']))

        for module in modules:
            validator = ParamsValidator(module['module'], self._modules_registry)
            # TODO: постараться переделать
            params = await validator.get_params(module['params'], private_key, proxy)
            network = params.get_chain()

            if self._config['CHECK_GWEI']:
                await wait_gwei(self._config['MAX_GWEI'], self._config['SLEEP_BETWEEN_GWEI_CHECKS'])

            client = await Client(private_key, convert_to_web3_network(network), proxy)
            module_instance = self._module_factory.get_module(module['module'], client, params)
            # Executing module
            module_result = await module_instance.execute()
            if not await module_instance.verify():
                pass

            # SLEEP_BETWEEN_MODULES
            min_sleep, max_sleep = self._config['SLEEP_BETWEEN_MODULES']
            sleep_time = random.uniform(min_sleep, max_sleep)
            logger.info(f"Sleeping for {sleep_time:.2f} seconds between modules")
            await asyncio.sleep(sleep_time)

            module_type = self._module_factory.get_module_type(module['module'])

            result = {module_type: module_result}

            self._wallet_histories[wallet_address].append(result)

    async def _process_wallet_via_module(self, private_key, module_name):
        wallet_address = get_wallet_address_from_private_key(private_key)
        wallet_address_var.set(wallet_address)

        proxy = await self._proxy_manager.get_random_proxy()
        self._wallet_histories[wallet_address] = []

        module_config = self._config['MODULES'].get(module_name)
        if not module_config:
            logger.error(f"No configuration found for module {module_name}")
            return

        validator = ParamsValidator(module_name, self._modules_registry)
        params = await validator.get_params(module_config, private_key, proxy)

        network = params.get_chain()

        if self._config['CHECK_GWEI']:
            await wait_gwei(self._config['MAX_GWEI'], self._config['SLEEP_BETWEEN_GWEI_CHECKS'])

        client = await Client(private_key, convert_to_web3_network(network), proxy)
        module_instance = self._module_factory.get_module(module_name, client, params)
        module_result = await module_instance.execute()

        if not await module_instance.verify():
            pass

        module_type = self._module_factory.get_module_type(module_name)
        result = {module_type: module_result}
        self._wallet_histories[wallet_address].append(result)

        min_sleep, max_sleep = self._config['SLEEP_BETWEEN_MODULES']
        sleep_time = random.uniform(min_sleep, max_sleep)
        logger.info(f"Sleeping for {sleep_time:.2f} seconds after executing module {module_name}")
        await asyncio.sleep(sleep_time)
