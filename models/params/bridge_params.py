import logging
import random

from w3.core import Client

from adapters.network_adapter import convert_to_web3_network
from models.interfaces.iparams import IParams
from models.network import Network
from models.token import Token
from utils.async_mixin import AsyncMixin

logger = logging.getLogger(__name__)

class BridgeParams(AsyncMixin, IParams):
    async def __ainit__(self, params: dict[str, any], validator, private_key: str, proxy: str) -> None:
        self.from_network: Network = validator.validate_network(params['from_network'])
        self.to_network: Network = validator.validate_network(params['to_network'])

        self.token: Token = validator.validate_token(self.from_network, params['token'])
        validator.validate_token(self.to_network, params['token'])

        if self.from_network == self.to_network:
            raise ValueError(
                f"Cannot bridge token from same network '{self.from_network.name}' to network {self.to_network.name}. "
                f"Please choose different networks for bridge."
            )

        client = await Client(private_key, convert_to_web3_network(self.from_network), proxy)

        balance = (await client.wallet.get_balance(self.token.address)).get_converted_amount()
        logger.info(f"Balance: {balance}")

        amount_from = self._parse_amount(params['amount_from'], balance, params['bridge_all_balance'])
        amount_to = self._parse_amount(params['amount_to'], balance, params['bridge_all_balance'])

        if amount_from > amount_to:
            raise ValueError(f"'amount_from' ({amount_from}) cannot be greater than 'amount_to' ({amount_to})")

        self.amount = random.uniform(amount_from, amount_to)
        logger.info(f"Randomly selected amount: {self.amount}")

        if self.amount <= 0:
            raise ValueError(f"Calculated amount is negative or 0: {self.amount}")

        if self.amount < params['bridge_all_balance']:
            raise ValueError(
                f"Selected amount ({self.amount}) is less than the minimum amount to swap ({params['min_amount_swap']})"
            )

    def __repr__(self):
        return (
            f"BridgeParams(network={self.from_network}, from_token={self.to_network}, "
            f"to_token={self.token}, amount={self.amount}"
        )

    def get_chain(self) -> Network:
        return self.from_network

    @staticmethod
    def _parse_amount(amount_str: str, total_balance: float, swap_all_balance: bool) -> float:
        if amount_str.endswith("%"):
            try:
                percentage = float(amount_str.strip('%')) / 100.0
            except ValueError:
                raise ValueError(f"Invalid percentage value: {amount_str}")

            if swap_all_balance:
                amount_to_remain = total_balance * percentage
                amount_to_transfer = total_balance - amount_to_remain
            else:
                amount_to_transfer = total_balance * percentage
        else:
            try:
                amount_value = float(amount_str)
            except ValueError:
                raise ValueError(f"Invalid amount value: {amount_str}")

            if swap_all_balance:
                amount_to_remain = amount_value
                amount_to_transfer = total_balance - amount_to_remain
            else:
                amount_to_transfer = amount_value

        if amount_to_transfer > total_balance:
            raise ValueError(f"Amount ({amount_to_transfer}) for transfer is greater than balance ({total_balance})")

        return amount_to_transfer