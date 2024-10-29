import asyncio
import logging

import aiohttp
import requests
from models.interfaces.ibridge import IBridge
from w3.core.client import Client
from models.params.bridge_params import BridgeParams
from .config_orbiter import ORBITER_CONTRACT_ADDRESSES, abi_orbiter

logger = logging.getLogger(__name__)

ORBITER_API_URL = "https://api.orbiter.finance/sdk/routers/v2"

class Orbiter(IBridge):

    async def bridge(self) -> dict:
        contract_address = ORBITER_CONTRACT_ADDRESSES.get(self._params.from_network.name)
        if contract_address is None:
            raise ValueError(f"No contract available for the network {self._params.from_network.name}")

        routes_data = await self._fetch_routes_data()
        call_id, endpoint = await self._get_call_id_and_endpoint(routes_data)

        data = f'c={call_id}&t={self._client.wallet.public_key}'
        data_bytes = data.encode('utf-8')
        data_hex = f'0x{data_bytes.hex()}'

        contract_address = self._client.w3.async_w3.to_checksum_address(contract_address)
        endpoint_address = self._client.w3.async_w3.to_checksum_address(endpoint)
        contract = self._client.contracts.get_contract(abi_orbiter, contract_address)

        encoded_data = contract.encode_abi(
            'transfer',
            args=(
                endpoint_address, data_hex
            )
        )

        amount_in_wei = int(self._client.w3.async_w3.to_wei(self._params.amount, 'ether'))

        await self._client.transactions.send(encoded_data, contract_address, amount_in_wei)

        logger.info(f"Bridge successful: {self._params.amount} {self._params.token.symbol} from {self._params.from_network.name} to {self._params.to_network.name}")
        return {
            'token': self._params.token,
            'from_network': self._params.from_network.name,
            'to_network': self._params.to_network.name,
            'amount': self._params.amount
        }

    async def _fetch_routes_data(self):
        """Fetch route data from the Orbiter API"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url=ORBITER_API_URL, proxy=self._client.w3.proxy) as response:
                    response.raise_for_status()
                    data = await response.json()
            except aiohttp.ClientError as e:
                raise Exception(f"Error fetching data from the Orbiter API: {str(e)}")
            except Exception as e:
                raise Exception(f"Unexpected error: {str(e)}")

        if data["status"] != "success":
            raise Exception(f"Error in the API response: {data['message']}")

        return data["result"]

    async def _get_call_id_and_endpoint(self, routes_data):
        """Extract call_id and endpoint from API data"""
        line_to_find = f"{self._params.from_network.chain_id}/{self._params.to_network.chain_id}-{self._params.token.symbol}/{self._params.token.symbol}"
        for route in routes_data:
            if route["line"] == line_to_find and route["state"] == "available":
                return route["vc"], route["endpoint"]

        raise ValueError(
            f"No available routes from {self._params.from_network.name} to {self._params.to_network.name}"
        )
