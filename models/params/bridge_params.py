import logging
import random

from w3.core import Client

from models.interfaces.iparams import IParams
from models.network import Network
from models.token import Token
from validators.params_validator import ParamsValidator

logger = logging.getLogger(__name__)

class BridgeParams(IParams):
    def __init__(self, params: dict, validator: ParamsValidator):
        self._params = params
        self._validator = validator
        self.from_network: Network
        self.to_network: Network
        self.token: Token
        self.amount: float

    def validate_selection_params(self, supported_chains: dict) -> None:
        self.from_network: Network = self._validator.validate_network(self._params['from_network'])
        self.to_network: Network = self._validator.validate_network(self._params['to_network'])

        self.token: Token = self._validator.validate_token(self.from_network, self._params['token'])
        self._validator.validate_token(self.to_network, self._params['token'])

        if self.from_network == self.to_network:
            raise ValueError(
                f"Cannot bridge token from same network '{self.from_network.name}' to network {self.to_network.name}. "
                f"Please choose different networks for bridge."
            )

        # Проверка поддержки токена модулем в обеих сетях
        from_supported_tokens = [token.lower() for token in supported_chains[self.from_network.name]]
        to_supported_tokens = [token.lower() for token in supported_chains[self.to_network.name]]

        if self.token.symbol.lower() not in from_supported_tokens:
            raise ValueError(f"Token '{self.token.symbol}' is not supported on network '{self.from_network.name}' by the module.")
        if self.token.symbol.lower() not in to_supported_tokens:
            raise ValueError(f"Token '{self.token.symbol}' is not supported on network '{self.to_network.name}' by the module.")

    async def validate_amount_params(self, client: Client) -> None:
        balance = (await client.wallet.get_balance(self.token.address)).get_converted_amount()
        logger.info(f"Balance: {balance}")

        bridge_all_balance = self._params.get('bridge_all_balance', False)
        if bridge_all_balance:
            amount_from = self._parse_amount(self._params.get('amount_to'), balance, bridge_all_balance)
            amount_to = self._parse_amount(self._params.get('amount_from'), balance, bridge_all_balance)
        else:
            amount_from = self._parse_amount(self._params.get('amount_from'), balance, bridge_all_balance)
            amount_to = self._parse_amount(self._params.get('amount_to'), balance, bridge_all_balance)

        if amount_from > amount_to:
            raise ValueError(f"'amount_from' ({amount_from}) cannot be greater than 'amount_to' ({amount_to}).")

        self.amount = random.uniform(amount_from, amount_to)
        logger.info(f"Randomly selected amount: {self.amount:.5f}")

        if self.amount <= 0:
            raise ValueError(f"Calculated amount is negative or zero: {self.amount}")

        min_amount_bridge = self._params.get('min_amount_bridge', 0)
        if self.amount < min_amount_bridge:
            raise ValueError(f"Selected amount ({self.amount}) is less than the minimum amount to bridge ({min_amount_bridge}).")

    def __repr__(self):
        return (
            f"BridgeParams(from_network={self.from_network}, to_network={self.to_network}, "
            f"token={self.token}, amount={self.amount})"
        )

    def get_chain(self) -> Network:
        return self.from_network

    @staticmethod
    def _parse_amount(amount_str: str, total_balance: float, bridge_all_balance: bool) -> float:
        if not amount_str:
            raise ValueError("Amount parameter is required.")
        if isinstance(amount_str, str) and amount_str.endswith("%"):
            try:
                percentage = float(amount_str.strip('%')) / 100.0
            except ValueError:
                raise ValueError(f"Invalid percentage value: {amount_str}")

            amount_to_transfer = total_balance * percentage
            if bridge_all_balance:
                amount_to_transfer = total_balance - amount_to_transfer
        else:
            try:
                amount_to_transfer = float(amount_str)
            except (ValueError, TypeError):
                raise ValueError(f"Invalid amount value: {amount_str}")

            if bridge_all_balance:
                amount_to_transfer = total_balance - amount_to_transfer

        if amount_to_transfer > total_balance:
            raise ValueError(f"Amount ({amount_to_transfer}) is greater than the total balance ({total_balance}).")

        return amount_to_transfer