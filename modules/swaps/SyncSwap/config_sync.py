from web3 import Web3

ETH_ADDRESS = '0x0000000000000000000000000000000000000000'

NETWORKS = {
    'ZKSync': {
        'rpc_url': 'https://1rpc.io/zksync2-era',
        'chain_id': 324,
        'contract_address': Web3.to_checksum_address('0x9B5def958d0f3b6955cBEa4D5B7809b2fb26b059'),
        'weth_address': Web3.to_checksum_address('0x5aea5775959fbc2557cc8789bc1bf90a239d9a91'),
        'use_vault_false_pools': [
            Web3.to_checksum_address('0xCeF016DaEF54E038c0d80e6C0f31BC6C8C98b7CA'),
        ],
        'tokens': {
            'USDC': {
                'address': Web3.to_checksum_address('0x3355df6d4c9c3035724fd0e3914de96a5a83aaf4'),
                'decimals': 6,
            },
            'USDT': {
                'address': Web3.to_checksum_address('0x493257fd37edb34451f62edf8d2a0c418852ba4c'),
                'decimals': 6,
            },
            'WBTC': {
                'address': Web3.to_checksum_address('0xbbeb516fb02a01611cbbe0453fe3c580d7281011'),
                'decimals': 8,
            },
            'ETH': {
                'address': ETH_ADDRESS,
                'decimals': 18,
            },
        },
        'pools': {
            'USDC-ETH': Web3.to_checksum_address('0x80115c708e12edd42e504c1cd52aea96c547c05c'),
            'USDT-ETH': Web3.to_checksum_address('0xCeF016DaEF54E038c0d80e6C0f31BC6C8C98b7CA'),
            'WBTC-ETH': Web3.to_checksum_address('0xb3479139e07568ba954c8a14d5a8b3466e35533d'),
        },
    },
    'Linea': {
        'rpc_url': 'https://linea-rpc.publicnode.com',
        'chain_id': 59144,
        'contract_address': Web3.to_checksum_address('0xC2a1947d2336b2AF74d5813dC9cA6E0c3b3E8a1E'),
        'weth_address': Web3.to_checksum_address('0xe5d7c2a44ffddf6b295a15c148167daaaf5cf34f'),
        'use_vault_false_pools': [
            Web3.to_checksum_address('0xDDed227D71A096c6B5D87807C1B5C456771aAA94'),
        ],
        'tokens': {
            'USDC': {
                'address': Web3.to_checksum_address('0x176211869ca2b568f2a7d4ee941e073a821ee1ff'),
                'decimals': 6,
            },
            'USDT': {
                'address': Web3.to_checksum_address('0xa219439258ca9da29e9cc4ce5596924745e12b93'),
                'decimals': 6,
            },
            'WBTC': {
                'address': Web3.to_checksum_address('0x3aab2285ddcddad8edf438c1bab47e1a9d05a9b4'),
                'decimals': 8,
            },
            'ETH': {
                'address': ETH_ADDRESS,
                'decimals': 18,
            },
        },
        'pools': {
            'USDC-ETH': Web3.to_checksum_address('0xDDed227D71A096c6B5D87807C1B5C456771aAA94'),
            'USDT-ETH': Web3.to_checksum_address('0x8aeBfFB3964ec5CEA0915080ddc1aCA079583a4d'),
            'WBTC-ETH': Web3.to_checksum_address('0xF5783661C3BAC33373ecF8977Fc0Df1FEb7886fa'),
        },
    },
    'Scroll': {
        'rpc_url': 'https://scroll-mainnet.public.blastapi.io',
        'chain_id': 534352,
        'contract_address': Web3.to_checksum_address('0xFD541D0e2773a189450A70F06bC7eDd3C1DC9115'),
        'weth_address': Web3.to_checksum_address('0x5300000000000000000000000000000000000004'),
        'use_vault_false_pools': [
            Web3.to_checksum_address('0xdf4E1bE5097f7756A015467163EFd77Dc1A22A39'),
            Web3.to_checksum_address('0xc650765659df198ffe9afc6A6109378c55E741d0'),
        ],
        'tokens': {
            'USDC': {
                'address': Web3.to_checksum_address('0x06efdbff2a14a7c8e15944d1f4a48f9f95f663a4'),
                'decimals': 6,
            },
            'USDT': {
                'address': Web3.to_checksum_address('0xf55bec9cafdbe8730f096aa55dad6d22d44099df'),
                'decimals': 6,
            },
            'WBTC': {
                'address': Web3.to_checksum_address('0x3c1bca5a656e69edcd0d4e36bebb3fcdaca60cf1'),
                'decimals': 8,
            },
            'ETH': {
                'address': ETH_ADDRESS,
                'decimals': 18,
            },
        },
        'pools': {
            'USDC-ETH': Web3.to_checksum_address('0x814A23B053FD0f102AEEda0459215C2444799C70'),
            'USDT-ETH': Web3.to_checksum_address('0xdf4E1bE5097f7756A015467163EFd77Dc1A22A39'),
            'WBTC-ETH': Web3.to_checksum_address('0xc650765659df198ffe9afc6A6109378c55E741d0'),
        },
    },
}
abi = [{"inputs":[{"internalType":"address","name":"_vault","type":"address"},{"internalType":"address","name":"_wETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"ApproveFailed","type":"error"},{"inputs":[],"name":"ETHTransferFailed","type":"error"},{"inputs":[],"name":"Expired","type":"error"},{"inputs":[],"name":"NotEnoughLiquidityMinted","type":"error"},{"inputs":[],"name":"TooLittleReceived","type":"error"},{"inputs":[],"name":"TransferFailed","type":"error"},{"inputs":[],"name":"TransferFromFailed","type":"error"},{"anonymous":'false',"inputs":[{"indexed":'true',"internalType":"address","name":"previousOwner","type":"address"},{"indexed":'true',"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"inputs":[{"internalType":"address","name":"pool","type":"address"},{"components":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bool","name":"useVault","type":"bool"}],"internalType":"struct SyncSwapRouterV2.TokenInput[]","name":"inputs","type":"tuple[]"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"uint256","name":"minLiquidity","type":"uint256"},{"internalType":"address","name":"callback","type":"address"},{"internalType":"bytes","name":"callbackData","type":"bytes"},{"internalType":"address","name":"staking","type":"address"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"pool","type":"address"},{"components":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bool","name":"useVault","type":"bool"}],"internalType":"struct SyncSwapRouterV2.TokenInput[]","name":"inputs","type":"tuple[]"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"uint256","name":"minLiquidity","type":"uint256"},{"internalType":"address","name":"callback","type":"address"},{"internalType":"bytes","name":"callbackData","type":"bytes"},{"internalType":"address","name":"staking","type":"address"}],"name":"addLiquidity2","outputs":[{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"pool","type":"address"},{"components":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bool","name":"useVault","type":"bool"}],"internalType":"struct SyncSwapRouterV2.TokenInput[]","name":"inputs","type":"tuple[]"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"uint256","name":"minLiquidity","type":"uint256"},{"internalType":"address","name":"callback","type":"address"},{"internalType":"bytes","name":"callbackData","type":"bytes"},{"components":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"approveAmount","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"internalType":"struct IRouter.SplitPermitParams[]","name":"permits","type":"tuple[]"},{"internalType":"address","name":"staking","type":"address"}],"name":"addLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"pool","type":"address"},{"components":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bool","name":"useVault","type":"bool"}],"internalType":"struct SyncSwapRouterV2.TokenInput[]","name":"inputs","type":"tuple[]"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"uint256","name":"minLiquidity","type":"uint256"},{"internalType":"address","name":"callback","type":"address"},{"internalType":"bytes","name":"callbackData","type":"bytes"},{"components":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"approveAmount","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"internalType":"struct IRouter.SplitPermitParams[]","name":"permits","type":"tuple[]"},{"internalType":"address","name":"staking","type":"address"}],"name":"addLiquidityWithPermit2","outputs":[{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"pool","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"uint256[]","name":"minAmounts","type":"uint256[]"},{"internalType":"address","name":"callback","type":"address"},{"internalType":"bytes","name":"callbackData","type":"bytes"}],"name":"burnLiquidity","outputs":[{"components":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"internalType":"struct IPool.TokenAmount[]","name":"amounts","type":"tuple[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"pool","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"uint256","name":"minAmount","type":"uint256"},{"internalType":"address","name":"callback","type":"address"},{"internalType":"bytes","name":"callbackData","type":"bytes"}],"name":"burnLiquiditySingle","outputs":[{"components":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"internalType":"struct IPool.TokenAmount","name":"amountOut","type":"tuple"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"pool","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"uint256","name":"minAmount","type":"uint256"},{"internalType":"address","name":"callback","type":"address"},{"internalType":"bytes","name":"callbackData","type":"bytes"},{"components":[{"internalType":"uint256","name":"approveAmount","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bytes","name":"signature","type":"bytes"}],"internalType":"struct IRouter.ArrayPermitParams","name":"permit","type":"tuple"}],"name":"burnLiquiditySingleWithPermit","outputs":[{"components":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"internalType":"struct IPool.TokenAmount","name":"amountOut","type":"tuple"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"pool","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"uint256[]","name":"minAmounts","type":"uint256[]"},{"internalType":"address","name":"callback","type":"address"},{"internalType":"bytes","name":"callbackData","type":"bytes"},{"components":[{"internalType":"uint256","name":"approveAmount","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bytes","name":"signature","type":"bytes"}],"internalType":"struct IRouter.ArrayPermitParams","name":"permit","type":"tuple"}],"name":"burnLiquidityWithPermit","outputs":[{"components":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"internalType":"struct IPool.TokenAmount[]","name":"amounts","type":"tuple[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"createPool","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"enteredPools","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"enteredPoolsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"isPoolEntered","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes[]","name":"data","type":"bytes[]"}],"name":"multicall","outputs":[{"internalType":"bytes[]","name":"results","type":"bytes[]"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"rescueERC20","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address payable","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"rescueETH","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermit","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bytes","name":"signature","type":"bytes"}],"name":"selfPermit2","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bytes","name":"signature","type":"bytes"}],"name":"selfPermit2IfNecessary","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"expiry","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermitAllowed","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"expiry","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermitAllowedIfNecessary","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermitIfNecessary","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"target","type":"address"},{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"to","type":"address"}],"name":"stake","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"target","type":"address"},{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"to","type":"address"}],"name":"stakeWithToken","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"components":[{"internalType":"address","name":"pool","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"address","name":"callback","type":"address"},{"internalType":"bytes","name":"callbackData","type":"bytes"},{"internalType":"bool","name":"useVault","type":"bool"}],"internalType":"struct IRouter.SwapStep[]","name":"steps","type":"tuple[]"},{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"uint256","name":"amountIn","type":"uint256"}],"internalType":"struct IRouter.SwapPath[]","name":"paths","type":"tuple[]"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swap","outputs":[{"components":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"internalType":"struct IPool.TokenAmount","name":"amountOut","type":"tuple"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"components":[{"internalType":"address","name":"pool","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"address","name":"callback","type":"address"},{"internalType":"bytes","name":"callbackData","type":"bytes"},{"internalType":"bool","name":"useVault","type":"bool"}],"internalType":"struct IRouter.SwapStep[]","name":"steps","type":"tuple[]"},{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"uint256","name":"amountIn","type":"uint256"}],"internalType":"struct IRouter.SwapPath[]","name":"paths","type":"tuple[]"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"components":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"approveAmount","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"internalType":"struct IRouter.SplitPermitParams","name":"permit","type":"tuple"}],"name":"swapWithPermit","outputs":[{"components":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"internalType":"struct IPool.TokenAmount","name":"amountOut","type":"tuple"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"vault","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"wETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]

erc20_abi = [
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"name": "_spender", "type": "address"},
            {"name": "_value", "type": "uint256"},
        ],
        "name": "approve",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {"name": "_owner", "type": "address"},
            {"name": "_spender", "type": "address"}
        ],
        "name": "allowance",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function",
    }
]
