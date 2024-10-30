import logging

from w3.core import Client

from configs.networks import Networks
from models.interfaces.iparams import IParams
from models.network import Network
from validators.params_validator import ParamsValidator

logger = logging.getLogger(__name__)

class ZoraMintParams(IParams):
    def __init__(self, params: dict, validator: ParamsValidator):
        self._params = params
        self._validator = validator
        self.network = Networks.ZORA
        self.min_mint_count: int
        self.max_mint_count: int

        self.min_mint_price: float
        self.max_mint_price: float

    def validate_selection_params(self, supported_chains: dict) -> None:
        self.min_mint_count = self._params['min_mint_count']
        self.max_mint_count = self._params['min_mint_count']

    async def validate_amount_params(self, client: Client) -> None:
        self.min_mint_price = self._params['min_mint_price']
        self.max_mint_price = self._params['max_mint_price']

    def __repr__(self):
        return (
            f"SwapParams(network={self.network}, min_mint_count={self.min_mint_count}, max_mint_count={self.max_mint_count}, "
            f"min_mint_price={self.min_mint_price}, max_mint_price={self.max_mint_price})"
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