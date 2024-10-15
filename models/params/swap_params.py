import logging
import random

from w3.core import Client

from adapters.network_adapter import convert_to_web3_network
from models.interfaces.iparams import IParams
from models.network import Network
from models.token import Token
from utils.async_mixin import AsyncMixin

logger = logging.getLogger(__name__)

class SwapParams(AsyncMixin, IParams):
    async def __ainit__(self, params: dict[str, any], validator, private_key: str, proxy: str) -> None:
        self.network: Network = validator.validate_network(params['network'])
        self.from_token: Token = validator.validate_token(self.network, params['from_token'])
        self.to_token: Token = validator.validate_token(self.network, params['to_token'])

        if self.from_token == self.to_token:
            raise ValueError(
                f"Cannot swap the same token '{self.from_token.symbol}' on network {self.network.name}. "
                f"Please choose different tokens for swapping."
            )

        client = await Client(private_key, convert_to_web3_network(self.network), proxy)

        balance = (await client.wallet.get_balance(self.from_token.address)).get_converted_amount()
        logger.info(f"Balance: {balance}")

        amount_from = self._parse_amount(params['amount_from'], balance, params['swap_all_balance'])
        amount_to = self._parse_amount(params['amount_to'], balance, params['swap_all_balance'])

        if amount_from > amount_to:
            raise ValueError(f"'amount_from' ({amount_from}) cannot be greater than 'amount_to' ({amount_to})")

        self.amount = random.uniform(amount_from, amount_to)
        logger.info(f"Randomly selected amount: {self.amount}")

        if self.amount <= 0:
            raise ValueError(f"Calculated amount is negative or 0: {self.amount}")

        if self.amount < params['min_amount_swap']:
            raise ValueError(
                f"Selected amount ({self.amount}) is less than the minimum amount to swap ({params['min_amount_swap']})"
            )

    def __repr__(self):
        return (
            f"SwapParams(network={self.network}, from_token={self.from_token}, "
            f"to_token={self.to_token}, amount={self.amount}"
        )

    def get_chain(self) -> Network:
        return self.network

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