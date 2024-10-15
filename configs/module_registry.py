from models.enums.module_type import ModuleType
from modules.bridges.Orbiter.orbiter import Orbiter
from modules.swaps.SyncSwap.sync_swap import SyncSwap

modules_registry = {
    'SyncSwap': {
        'type': ModuleType.SWAP,
        'class': SyncSwap,
        'supported_chains': {
            'ZKSync': ['eth', 'usdc', 'usdt', 'usdc.e', 'wbtc', 'weth'],
            'Linea': ['eth', 'usdc', 'usdt', 'wbtc', 'weth'],
            'Scroll': ['eth', 'usdc', 'usdt', 'wbtc', 'weth'],
        },
    },
    'Orbiter': {
        'type': ModuleType.BRIDGE,
        'class': Orbiter,
        'supported_chains': {
            'Ethereum': ['eth', 'usdc'],
            'Optimism': ['eth', 'usdc', 'usdt'],
            'BSC': ['eth', 'usdc', 'usdt'],
            'Polygon': ['eth', 'usdc', 'usdt'],
            'Arbitrum': ['eth', 'usdc', 'usdt'],
            'ZKSync': ['eth', 'usdc', 'usdt'],
            'Linea': ['eth', 'usdc', 'usdt'],
            'Base': ['eth', 'usdc'],
            'Zora': ['eth'],
            'Scroll': ['eth', 'usdc', 'usdt', 'wbtc', 'weth'],
            'Blast': ['eth'],
            'OpBNB': ['eth'],
        },
    },
}