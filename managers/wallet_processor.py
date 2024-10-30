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
        self._wallet_histories: dict = {}
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
        self._wallet_histories[wallet_address] = []

        scenario_name = self._config['SCENARIO']
        scenario = self._scenario_manager.get_scenario(scenario_name)
        scenario_type = scenario['type']

        modules = scenario['module_sequence'] if scenario_type == 'STRICT' else random.sample(
            scenario['module_sequence'], len(scenario['module_sequence']))

        for module in modules:
            if self._config['CHECK_GWEI']:
                await wait_gwei(self._config['MAX_GWEI'], self._config['SLEEP_BETWEEN_GWEI_CHECKS'])

            module_name_or_type = module['module']
            params = module['params']

            proxy = await self._proxy_manager.get_random_proxy()

            module_instance = await self._module_factory.create_module_instance(
                module_name_or_type,
                params,
                private_key,
                proxy
            )

            module_result = await module_instance.execute()

            # Wait for the module execution to complete
            wait_time_minutes = self._config['WAIT_EXECUTION_MODULE']
            success = await self.wait_for_module(module_instance, wait_time_minutes)

            if not success:
                logger.error(f"Module {module_name_or_type} did not complete within the expected time.")
                continue

            # SLEEP_BETWEEN_MODULES
            min_sleep, max_sleep = self._config['SLEEP_BETWEEN_MODULES']
            await self.wait_between_modules(min_sleep, max_sleep)

            module_type = self._module_factory.determine_module_type(module_name_or_type).name
            result = {module_type: module_result}
            self._wallet_histories[wallet_address].append(result)

    async def _process_wallet_via_module(self, private_key, module_name_or_type):
        wallet_address = get_wallet_address_from_private_key(private_key)

        wallet_address_var.set(wallet_address)
        self._wallet_histories[wallet_address] = []

        if self._config['CHECK_GWEI']:
            await wait_gwei(self._config['MAX_GWEI'], self._config['SLEEP_BETWEEN_GWEI_CHECKS'])

        params = self._config['MODULES'][module_name_or_type]

        proxy = await self._proxy_manager.get_random_proxy()

        module_instance = await self._module_factory.create_module_instance(
            module_name_or_type,
            params,
            private_key,
            proxy
        )

        module_result = await module_instance.execute()

        # Wait for the module execution to complete
        wait_time_minutes = self._config['WAIT_VERIFY_MODULE']
        success = await self.wait_for_module(module_instance, wait_time_minutes)

        if not success:
            logger.error(f"Module {module_name_or_type} did not complete within the expected time.")

        # SLEEP_BETWEEN_MODULES
        min_sleep, max_sleep = self._config['SLEEP_BETWEEN_MODULES']
        await self.wait_between_modules(min_sleep, max_sleep)

        module_type = self._module_factory.determine_module_type(module_name_or_type).name
        result = {module_type: module_result}
        self._wallet_histories[wallet_address].append(result)

    async def wait_between_modules(self, min_sleep, max_sleep):
        sleep_time = random.uniform(min_sleep, max_sleep)
        logger.info(f"Sleeping for {sleep_time:.2f} seconds between modules")
        await asyncio.sleep(sleep_time)

    async def wait_for_module(self, module_instance, timeout_minutes):
        total_wait_time = 0
        check_interval = 60

        while total_wait_time < timeout_minutes * 60:
            if await module_instance.verify():
                return True
            await asyncio.sleep(check_interval)
            total_wait_time += check_interval

        return False