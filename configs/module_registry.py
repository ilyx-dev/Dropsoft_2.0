from models.enums.module_type import ModuleType
from modules.bridges.Orbiter.orbiter import Orbiter
from modules.bridges.Owlto.owlto import Owlto
from modules.swaps.SyncSwap.sync_swap import SyncSwap
from modules.swaps.NullXSwap.null_x_swap import NullXSwap

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
    'Owlto': {
        'type': ModuleType.BRIDGE,
        'class': Owlto,
        'supported_chains': {
            'Ethereum': ['eth', 'usdc', 'usdt', 'wstETH', 'weETH'],
            'Zora': ['eth'],
            'Optimism': ['eth', 'usdc', 'usdt', 'wstETH'],
            'ZKSync': ['eth', 'usdc', 'usdt'],
            'Blast': ['eth', 'weETH'],
            'BSC': ['eth', 'usdc', 'usdt'],
            'OpBNB': ['eth'],
            'Metis': ['eth', 'usdc', 'usdt'],
            'Polygon': ['eth', 'usdc', 'usdt'],
            'Arbitrum': ['eth', 'usdc', 'usdt', 'wstETH', 'weETH'],
            'Linea': ['eth', 'usdc', 'usdt', 'wstETH', 'weETH'],
            'Base': ['eth', 'usdc'],
            'Scroll': ['eth', 'usdc', 'usdt', 'wstETH', 'weETH'],
        },
    },
    '0xSwap': {
        'type': ModuleType.SWAP,
        'class': NullXSwap,
        'supported_chains': {
            'Ethereum': ['eth', 'usdc', 'usdt', 'BNB', 'WBTC'],
            'Arbitrum': ['eth', 'usdc', 'usdt', 'usdc.e', 'WBTC'],
            'Avalanche': ['avax', 'eth', 'usdc', 'usdt'],
            'Base': ['eth', 'usdc', 'usdt'],
            'Blast': ['eth', 'usdc', 'usdt'],
            'BSC': ['eth', 'usdc', 'usdt'],
            'Linea': ['eth', 'usdc', 'usdt'],
            'Optimism': ['eth', 'usdc', 'usdt'],
            'Polygon': ['eth', 'usdc', 'usdt'],
            'Scroll': ['eth', 'usdc', 'usdt'],
        },
    },
}