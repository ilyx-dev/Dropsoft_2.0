import asyncio
import logging
import os
import sys
from datetime import datetime

from configs.module_registry import modules_registry
from managers.config_manager import ConfigManager
from managers.module_factory import ModuleFactory
from managers.proxy_manager import ProxyManager
from managers.scenario_manager import ScenarioManager
from managers.wallet_processor import WalletProcessor
from utils.contextvar import wallet_address_var
from utils.helpers import read_from_file, \
    read_and_decrypt_private_keys, get_path

logger = logging.getLogger(__name__)

scenarios_file = get_path("data/configs/scenarios.json")
config_file = get_path("data/configs/config.json")

private_keys_file = get_path("data/wallets.txt")
recipients_file = get_path("data/recipients.txt")
proxies_file = get_path("data/proxies.txt")

async def main():
    setup_logger()

    private_keys = read_and_decrypt_private_keys(private_keys_file, "NsaCEh833<-Y", "H.N~XyS)NnIP")
    recipients = read_from_file(recipients_file)
    proxies = read_from_file(proxies_file)

    try:
        validate_files(private_keys, recipients, proxies)
    except ValueError as e:
        logger.error(e)
        sys.exit(1)

    config_manager = ConfigManager(config_file)
    scenario_manager = ScenarioManager(scenarios_file)

    module_factory = ModuleFactory(modules_registry)
    proxy_manager = ProxyManager(proxies_file, config_manager.get_proxy_manager_config())
    executor = WalletProcessor(private_keys, recipients, proxy_manager, scenario_manager, module_factory, modules_registry, config_manager.get_wallet_processor_config())

    await executor.process_wallets()

def setup_logger():
    logging.getLogger('asyncio').setLevel(logging.CRITICAL)  # Скрываем логи asyncio

    log_dir = 'results/logs'
    os.makedirs(log_dir, exist_ok=True)

    start_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_filename = os.path.join(log_dir, f'log_{start_time}.log')

    file_handler = logging.FileHandler(log_filename, mode='w')
    console_handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-6s | %(name)-35s | %(wallet_address)-42s | %(message)s',
        datefmt='%m-%d %H:%M'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    file_handler.setLevel(logging.DEBUG)
    console_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    old_factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.wallet_address = wallet_address_var.get()
        return record

    logging.setLogRecordFactory(record_factory)

def validate_files(wallets, recipients, proxies):
    if not wallets:
        raise ValueError("Wallets file empty")
    if not recipients:
        raise ValueError("Recipients file empty")
    if not proxies:
        raise ValueError("Proxies file empty")

    if len(wallets) != len(recipients) or len(wallets) != len(proxies):
        raise ValueError("The number of elements in wallets, recipients, and proxies files does not match.")


if __name__ == '__main__':
    asyncio.run(main())
