class Token:
    def __init__(self, symbol: str, address: str | None = None):
        self.symbol = symbol
        self.address = address

    def __repr__(self):
        return f"Token(symbol={self.symbol}, address={self.address})"

    def __eq__(self, other):
        if isinstance(other, Token):
            return (self.symbol == other.symbol) and (self.address == other.address)
        return False