from enum import Enum


class ModuleType(Enum):
    SWAP = 'swap'
    BRIDGE = 'bridge'
    ZORA_MINT = 'zora_mint'
    CUSTOM = 'custom'