from models.network import Network
from models.token import Token


ethereum_tokens = [
    Token('ETH'),
    Token('USDT','0xdAC17F958D2ee523a2206206994597C13D831ec7'),
    Token('BNB','0xB8c77482e45F1F44dE1745F52C74426C631bDD52'),
    Token('USDC','0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'),
    Token('WBTC','0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599'),
]

optimism_tokens = [
    Token('ETH'),
    Token('USDT', '0x94b008aA00579c1307B0EF2c499aD98a8ce58e58'),
    Token('USDC', '0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85'),
    Token('USDC.e', '0x7F5c764cBc14f9669B88837ca1490cCa17c31607'),
    Token('LINK', '0x7F5c764cBc14f9669B88837ca1490cCa17c31607'),
    Token('WBTC', '0x68f180fcCe6836688e9084f035309E29Bf0A2095'),
]

bsc_tokens = [
    Token('BNB'),
    Token('ETH', '0x2170Ed0880ac9A755fd29B2688956BD959F933F8'),
    Token('BUSD-T', '0x55d398326f99059fF775485246999027B3197955'),
    Token('USDC', '0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d'),
    Token('BTCB', '0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c'),
]

polygon_tokens = [
    Token('WETH', '0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619'),
    Token('USDT', '0xc2132D05D31c914a87C6611C10748AEb04B58e8F'),
    Token('USDC', '0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359'),
    Token('USDC.e', '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174'),
    Token('WBTC', '0x1BFD67037B42Cf73acF2047067bd4F2C47D9BfD6'),
]

arbitrum_tokens = [
    Token('ETH', ''),
    Token('USDT', '0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9'),
    Token('USDC.e', '0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8'),
    Token('USDC', '0xaf88d065e77c8cC2239327C5EDb3A432268e5831'),
    Token('LINK', '0xf97f4df75117a78c1A5a0DBb814Af92458539FB4'),
    Token('WBTC', '0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f'),
]

avalanche_tokens = [
    Token('USDT', '0x9702230a8ea53601f5cd2dc00fdbc13d4df4a8c7'),
    Token('USDC', '0xb97ef9ef8734c71904d8002f8b6bc66dd9c48a6e'),
    Token('WBTC.e', '0x50b7545627a5162f82a992c33b87adc75187b218'),
    Token('TUSD', '0x1c20e891bab6b1727d14da358fae2984ed9b59eb'),
]

zksync_tokens= [
    Token('ETH'),
    Token('USDT', '0x493257fd37edb34451f62edf8d2a0c418852ba4c'),
    Token('USDC', '0x3355df6d4c9c3035724fd0e3914de96a5a83aaf4'),
    Token('WBTC', '0xBBeB516fb02a01611cBBE0453Fe3c580D7281011'),
    Token('DAI', '0x4b9eb6c0b6ea15176bbf62841c6b2a8a398cb656'),
]

linea_tokens = [
    Token('ETH'),
    Token('BUSD', '0x7d43AABC515C356145049227CeE54B608342c0ad'),
    Token('USDC.e', '0x176211869cA2b568f2A7D4EE941E073a821EE1ff'),
    Token('WBTC', '0x3aAB2285ddcDdaD8edf438C1bAB47e1a9D05a9b4'),
    Token('USDT', '0xA219439258ca9da29E9Cc4cE5596924745e12B93'),
    Token('wstETH', '0xB5beDd42000b71FddE22D3eE8a79Bd49A568fC8F'),
    Token('ezETH', '0x2416092f143378750bb29b79eD961ab195CcEea5'),
    Token('weETH', '0x1Bf74C010E6320bab11e2e5A532b5AC15e0b8aA6'),
    Token('wrsETH', '0xD2671165570f41BBB3B0097893300b6EB6101E6C'),
    Token('STONE', '0x93F4d0ab6a8B4271f4a28Db399b5E30612D21116'),
    Token('ZERO', '0x78354f8DcCB269a615A7e0a24f9B0718FDC3C7A7'),
]

#TODO: убрать нахуй
plug = [
    Token('bebraChlen', 'aye'),
]

class Networks:
    ETHEREUM = Network("Ethereum", ["https://rpc.ankr.com/eth"], 1, 2, ethereum_tokens)
    OPTIMISM = Network("Optimism", ["https://rpc.ankr.com/optimism"], 10, 2, optimism_tokens)
    BSC = Network("BSC", ["https://rpc.ankr.com/bsc"], 56, 0, bsc_tokens)
    POLYGON = Network("Polygon", ["https://rpc.ankr.com/polygon"], 137, 0, polygon_tokens)
    ARBITRUM = Network("Arbitrum", ["https://rpc.ankr.com/arbitrum"], 42161, 2, arbitrum_tokens)
    AVALANCHE = Network("Avalanche", ["https://rpc.ankr.com/avalanche"], 43114, 0, avalanche_tokens)
    ZKSYNC = Network("ZKSync", ["https://mainnet.era.zksync.io"], 324, 2, zksync_tokens)
    LINEA = Network("Linea", ["https://rpc.linea.build"], 59144, 0, linea_tokens)
    BASE = Network("Base", ["https://mainnet.base.org"], 8453, 2, plug)
    ZORA = Network("Zora", ["https://zora.rpc.thirdweb.com"], 7777777, 2, plug)
    SCROLL = Network("Scroll", ["https://scroll.blockpi.network/v1/rpc/public"], 534352, 0, plug)
    METIS = Network("Metis", ["https://metis-mainnet.public.blastapi.io"], 1088, 0, plug)
    BLAST = Network("Blast", ["https://blast.blockpi.network/v1/rpc/public"], 81457, 2, plug)
    OPBNB = Network("OpBNB", ["https://opbnb-rpc.publicnode.com"], 204, 2, plug)

    @staticmethod
    def from_str(network_str: str) -> Network:
        network_str = network_str.lower()

        for name, network in Networks.__dict__.items():
            if isinstance(network, Network):
                if network.name.lower() == network_str:
                    return network

        raise ValueError(f"Unknown network: {network_str}")