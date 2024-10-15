import random
import logging
from web3 import AsyncWeb3, AsyncHTTPProvider
from aiohttp import ClientResponseError
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

from utils.helpers import read_from_file

logger = logging.getLogger(__name__)

class ProxyManager:
    def __init__(self, proxies_path: str, rpcs_config: dict[str, [str]]):
        raw_proxies = read_from_file(proxies_path)

        self._rpcs = rpcs_config['RPCS_FOR_PROXY']
        self._proxies = []
        for proxy in raw_proxies:
            proxy = proxy.strip()
            if proxy.startswith('http://') or proxy.startswith('https://'):
                self._proxies.append(proxy)
            else:
                parts = proxy.split(':')
                if len(parts) == 4:
                    ip = parts[0]
                    port = parts[1]
                    username = parts[2]
                    password = parts[3]
                    formatted_proxy = f'http://{username}:{password}@{ip}:{port}'
                    self._proxies.append(formatted_proxy)
                else:
                    raise ValueError(f"Invalid proxy format: {proxy}")

    async def get_random_proxy(self):
        while True:
            random_proxy = random.choice(self._proxies)
            if await self._check_proxy(random_proxy):
                return random_proxy

    @retry(
        retry=retry_if_exception_type(ClientResponseError),  # Повторяем попытку при ClientResponseError
        wait=wait_fixed(2),  # Ждем 2 секунды между попытками
        stop=stop_after_attempt(3)  # Останавливаемся после 3 попыток
    )
    async def _check_proxy(self, proxy: str) -> bool:
        rpc = random.choice(self._rpcs)
        try:
            w3 = AsyncWeb3(AsyncHTTPProvider(rpc, request_kwargs={
                'proxy': proxy,
            }))
            if await w3.is_connected():
                logger.debug(f"Connected to {rpc} using proxy {proxy}")
                return True
            else:
                logger.debug(f"Connection failed to {rpc} using proxy {proxy}")
                return False
        except ClientResponseError as e:
            if e.status == 429:
                logger.warning(f"RPC {rpc} returned 'Too Many Requests' (429). Retrying...")
                raise e
            else:
                logger.debug(f"Failed to connect to {rpc} using proxy {proxy}: {e}")
                return False
        except Exception as e:
            logger.debug(f"An error occurred while connecting to {rpc} using proxy {proxy}: {e}")
            return False
