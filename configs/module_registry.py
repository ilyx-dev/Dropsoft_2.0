from models.enums.module_type import ModuleType
from models.params.zora_mint_params import ZoraMintParams
from modules.bridges.Nitro.nitro import Nitro
from modules.bridges.Orbiter.orbiter import Orbiter
from modules.bridges.Owlto.owlto import Owlto
from modules.bridges.Stargate.stargate import Stargate
from modules.bridges.Relay.reley import Relay
from modules.swaps.BaseSwap.base_swap import BaseSwap
from modules.swaps.SyncSwap.sync_swap import SyncSwap
from modules.swaps.ZeroXSwap.zero_x_swap import ZeroXSwap
from modules.swaps.OdosSwap.odos_swap import OdosSwap
from modules.swaps.OpenOceanSwap.open_ocean_swap import OpenOceanSwap
from modules.zora.zora_mint import ZoraMint

modules_registry = {
    'Zora.mint': {
        'type': ModuleType.CUSTOM,
        'class': ZoraMint,
        'params_class': ZoraMintParams
    },
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
    'Nitro': {
        'type': ModuleType.BRIDGE,
        'class': Nitro,
        'supported_chains': {
            'Ethereum': ['eth', 'usdc', 'usdt', 'WBTC', 'WETH'],
            'Optimism': ['eth', 'usdc', 'usdt', 'WBTC'],
            'ZKSync': ['eth', 'usdc', 'usdt', 'WETH', 'WBTC'],
            'Blast': ['eth'],
            'BSC': ['WETH', 'usdc', 'usdt'],
            'Metis': ['usdc', 'usdt'],
            'Polygon': ['WETH', 'usdc', 'usdt'],
            'Arbitrum': ['eth', 'usdc', 'usdt', 'wstETH', 'weETH'],
            'Linea': ['eth', 'usdc', 'usdt'],
            'Base': ['eth', 'usdc'],
            'Scroll': ['usdc', 'usdt'],
        },
    },
    '0xSwap': {
        'type': ModuleType.SWAP,
        'class': ZeroXSwap,
        'supported_chains': {
            'Ethereum': ['eth', 'usdc', 'usdt', 'BNB', 'WBTC'],
            'Arbitrum': ['eth', 'usdc', 'usdt', 'usdc.e', 'WBTC'],
            'Avalanche': ['avax', 'eth', 'usdc', 'usdt'],
            'Base': ['eth', 'usdc', 'usdt'],
            'Blast': ['eth', 'usdc', 'usdt'],
            'BSC': ['eth', 'usdc', 'usdt'],
            'Linea': ['eth', 'usdc', 'usdt', 'wstETH'],
            'Optimism': ['eth', 'usdc', 'usdt'],
            'Polygon': ['eth', 'usdc', 'usdt'],
            'Scroll': ['eth', 'usdc', 'usdt'],
        },
    },
    'BaseSwap': {
        'type': ModuleType.SWAP,
        'class': BaseSwap,
        'supported_chains': {
            'Base': ['eth', 'usdc', 'usdt', 'USDbC', 'weETH', 'wstETH', 'WETH', 'DOG', 'DAI', 'DAI+'],
        },
    },
    'Stargate': {
        'type': ModuleType.BRIDGE,
        'class': Stargate,
        'supported_chains': {
            'Ethereum': ['eth', 'usdc', 'usdt'],
            'Optimism': ['eth', 'usdc'],
            'BSC': ['usdt'],
            'Polygon': ['usdc', 'usdt'],
            'Arbitrum': ['eth', 'usdc', 'usdt'],
            'Linea': ['eth'],
            'Base': ['eth', 'usdc'],
            'Avalanche': ['usdc', 'usdt'],
        }
    },
    'Relay': {
        'type': ModuleType.BRIDGE,
        'class': Relay,
        'supported_chains': {
            'Ethereum': ['eth', 'usdc', 'usdt', 'WBTC', 'WETH'],
            'Optimism': ['eth','WBTC','WETH'],
            'ZKSync': ['eth', 'usdc', 'WETH', 'WBTC'],
            'Blast': ['eth', 'WETH',],
            'Polygon': ['WETH', 'usdt'],
            'Arbitrum': ['eth', 'usdc', 'usdt', 'WBTC', 'WETH'],
            'Linea': ['eth', 'WETH'],
            'Base': ['eth', 'usdc','WETH'],
            'Scroll': ['eth', 'WETH']
        }
    },
    'OdosSwap': {
        'type': ModuleType.SWAP,
        'class': OdosSwap,
        'supported_chains': {
            'Ethereum': ['eth', 'usdc', 'usdt', 'BNB', 'WBTC'],
            'Arbitrum': ['eth', 'usdc', 'usdt', 'usdc.e', 'WBTC'],
            'Avalanche': ['avax', 'eth', 'usdc', 'usdt'],
            'Base': ['eth', 'usdc', 'usdt'],
            'Linea': ['eth', 'usdc', 'usdt', 'wstETH'],
            'Optimism': ['eth', 'usdc', 'usdt'],
            'Polygon': ['eth', 'usdc', 'usdt'],
            'Scroll': ['eth', 'usdc', 'usdt'],
        },
    },
    'OpenOceanSwap': {
        'type': ModuleType.SWAP,
        'class': OpenOceanSwap,
        'supported_chains': {
            'Ethereum': ['eth', 'usdc', 'usdt', 'BNB', 'WBTC'],
            'Arbitrum': ['eth', 'usdc', 'usdt', 'usdc.e', 'WBTC'],
            'Avalanche': ['avax', 'eth', 'usdc', 'usdt'],
            'Base': ['eth', 'usdc', 'usdt'],
            'Linea': ['eth', 'usdc', 'usdt', 'wstETH'],
            'Optimism': ['eth', 'usdc', 'usdt'],
            'Polygon': ['eth', 'usdc', 'usdt'],
            'Scroll': ['eth', 'usdc', 'usdt'],
            'Zksync': ['eth', 'usdt', 'usdc', 'wbtc'],
            'BSC': ['eth', 'usdc', 'usdt'],
            'Blast': ['eth', 'usdc', 'usdt'],
        },
    },
}
