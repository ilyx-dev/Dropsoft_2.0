from dataclasses import dataclass
from typing import List, Literal

from models.token import Token

@dataclass
class Network:
    name: str
    rpcs: List[str]
    chain_id: int
    tx_type: Literal[0, 2]
    tokens: List[Token]

    def __repr__(self):
        return (f"Network(name={self.name}, rpcs={self.rpcs}, "
                f"chain_id={self.chain_id}, "
                f"tx_type={self.tx_type}, tokens={self.tokens})")

    def get_token_by_symbol(self, symbol: str) -> Token:
        for token in self.tokens:
            if token.symbol.lower() == symbol.lower():
                return token
        raise ValueError(f"Token {symbol} not found in network {self.name}")