from models.enums.module_type import ModuleType
from models.params.bridge_params import BridgeParams
from models.params.swap_params import SwapParams

module_type_to_params_class = {
    ModuleType.SWAP: SwapParams,
    ModuleType.BRIDGE: BridgeParams,
}