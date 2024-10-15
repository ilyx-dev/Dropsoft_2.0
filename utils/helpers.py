import asyncio
import json
import logging
import os
import random
import sys

from web3 import AsyncWeb3, AsyncHTTPProvider

from configs.networks import Networks

logger = logging.getLogger(__name__)


def read_from_file(path: str) -> list[str]:
    with open(path, "r") as f:
        return f.read().splitlines()


def convert_proxies(proxies: list[str]) -> list[str]:
    convert_proxies = []
    for line in proxies:
        parts = line.split(":")
        if len(parts) == 4:
            ip = parts[0]
            port = parts[1]
            username = parts[2]
            password = parts[3]

            formatted_proxy = f"http://{username}:{password}@{ip}:{port}"
            convert_proxies.append(formatted_proxy)
        else:
            raise ValueError(f"Invalid proxy format: {line}")
    return convert_proxies


def read_and_decrypt_private_keys(file_path: str, password: str, salt: str) -> list[str]:
    decrypted_keys = []

    with open(file_path, "r") as f:
        for line in f.read().splitlines():
            try:
                decrypted_key = decrypt_string(line, password, salt)
            except Exception:
                raise ValueError(f"Invalid private key format: {line}")
            decrypted_keys.append(decrypted_key)

    return decrypted_keys


def decrypt_string(encrypted_text: str, password: str, salt: str) -> str:
    encrypted_text = bytes.fromhex(encrypted_text).decode('utf-8')

    decrypted_text = []
    password_length = len(password)
    salt_length = len(salt)

    for i, char in enumerate(encrypted_text[::2]):
        decrypted_char = chr(
            ord(char) ^ ord(password[i % password_length]) ^ ord(salt[(i + password_length) % salt_length])
        )
        decrypted_text.append(decrypted_char)

    return ''.join(decrypted_text)


def read_json_file(file: str) -> dict:
    with open(file) as f:
        return json.load(f)

def get_wallet_address_from_private_key(private_key: str) -> str:
    web3 = AsyncWeb3()
    account = web3.eth.account.from_key(private_key)
    return account.address

async def get_current_gwei():
    rpc_url = random.choice(Networks.ETHEREUM.rpcs)
    web3 = AsyncWeb3(AsyncHTTPProvider(rpc_url))
    gas_price_wei = await web3.eth.gas_price
    gas_price_gwei = web3.from_wei(gas_price_wei, 'gwei')
    return gas_price_gwei

async def wait_gwei(max_gwei: int, check_time: int):
    current_gwei = await get_current_gwei()
    while current_gwei > max_gwei:
        logger.info(f"Gwei {current_gwei} > MAX_GWEI {max_gwei}. Waiting...")
        await asyncio.sleep(check_time)
        current_gwei = await get_current_gwei()
    logger.info(f"Gwei {current_gwei} GOOD. Go")


def get_path(relative_path):
    if getattr(sys, '_MEIPASS', False):
        base_path = os.path.dirname(sys.executable)
        print(base_path)
    else:
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))

    return os.path.join(base_path, relative_path)
