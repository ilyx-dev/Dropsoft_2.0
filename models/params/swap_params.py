import logging
import random

from w3.core import Client

from models.interfaces.iparams import IParams
from models.network import Network
from models.token import Token
from validators.params_validator import ParamsValidator

logger = logging.getLogger(__name__)

class SwapParams(IParams):
    def __init__(self, params: dict, validator: ParamsValidator):
        self._params = params
        self._validator = validator
        self.network: Network
        self.from_token: Token
        self.to_token: Token
        self.amount: float

    def validate_selection_params(self, supported_chains: dict) -> None:
        # Валидация сети
        self.network: Network = self._validator.validate_network(self._params['network'])
        self.from_token: Token = self._validator.validate_token(self.network, self._params['from_token'])
        self.to_token: Token = self._validator.validate_token(self.network, self._params['to_token'])

        # Валидация токенов
        from_token_symbol = self.from_token.symbol.lower()
        to_token_symbol = self.to_token.symbol.lower()
        if not from_token_symbol or not to_token_symbol:
            raise ValueError("Parameters 'from_token' and 'to_token' are required.")

        if self.from_token == self.to_token:
            raise ValueError(f"Cannot swap the same token '{self.from_token.symbol}' on network '{self.network.name}'.")

        # Проверка поддержки токенов модулем
        supported_tokens = [token.lower() for token in supported_chains[self.network.name]]
        if from_token_symbol not in supported_tokens:
            raise ValueError(f"Token '{self.from_token.symbol}' is not supported on network '{self.network.name}' by the module.")
        if to_token_symbol not in supported_tokens:
            raise ValueError(f"Token '{self.to_token.symbol}' is not supported on network '{self.network.name}' by the module.")

    async def validate_amount_params(self, client: Client) -> None:
        balance = (await client.wallet.get_balance(self.from_token.address)).get_converted_amount()

        logger.info(f"Balance: {balance}")

        swap_all_balance = self._params.get('swap_all_balance', False)
        if swap_all_balance:
            amount_from = self._parse_amount(self._params.get('amount_to'), balance, swap_all_balance)
            amount_to = self._parse_amount(self._params.get('amount_from'), balance, swap_all_balance)
        else:
            amount_from = self._parse_amount(self._params.get('amount_from'), balance, swap_all_balance)
            amount_to = self._parse_amount(self._params.get('amount_to'), balance, swap_all_balance)

        if amount_from > amount_to:
            raise ValueError(f"'amount_from' ({amount_from}) cannot be greater than 'amount_to' ({amount_to}).")

        self.amount = random.uniform(amount_from, amount_to)
        logger.info(f"Randomly selected amount: {self.amount:.5f}")

        if self.amount <= 0:
            raise ValueError(f"Calculated amount is negative or zero: {self.amount}")

        min_amount_swap = self._params.get('min_amount_swap', 0)
        if self.amount < min_amount_swap:
            raise ValueError(f"Selected amount ({self.amount}) is less than the minimum amount to swap ({min_amount_swap}).")

    def __repr__(self):
        return (
            f"SwapParams(network={self.network}, from_token={self.from_token}, "
            f"to_token={self.to_token}, amount={self.amount})"
        )

    def get_chain(self) -> Network:
        return self.network

    @staticmethod
    def _parse_amount(amount_str: str, total_balance: float, swap_all_balance: bool) -> float:
        if not amount_str:
            raise ValueError("Amount parameter is required.")
        if isinstance(amount_str, str) and amount_str.endswith("%"):
            try:
                percentage = float(amount_str.strip('%')) / 100.0
            except ValueError:
                raise ValueError(f"Invalid percentage value: {amount_str}")

            amount_to_transfer = total_balance * percentage
            if swap_all_balance:
                amount_to_transfer = total_balance - amount_to_transfer
        else:
            try:
                amount_to_transfer = float(amount_str)
            except (ValueError, TypeError):
                raise ValueError(f"Invalid amount value: {amount_str}")

            if swap_all_balance:
                amount_to_transfer = total_balance - amount_to_transfer

        if amount_to_transfer > total_balance:
            raise ValueError(f"Amount ({amount_to_transfer}) is greater than the total balance ({total_balance}).")

        return amount_to_transfer