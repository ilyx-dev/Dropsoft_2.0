

# Маппинг адресов контрактов Orbiter для каждой сети
ORBITER_CONTRACT_ADDRESSES = {
    'ZKSync': '0xb4ab2ff34fadc774aff45f1c4566cb5e16bd4867',
    'Ethereum': '0xc741900276cd598060b0fe6594fbe977392928f4',
    'Arbitrum': '0x6a065083886ec63d274b8e1fe19ae2ddf498bfdd',
    'Polygon': '0x653f25dc641544675338cb47057f8ea530c69b78',
    'Optimism': '0x3191f40de6991b1bb1f61b7cec43d62bb337786b',
    'Scroll': '0x13e46b2a3f8512ed4682a8fb8b560589fe3c2172',
    'BSC': '0x13e46b2a3f8512ed4682a8fb8b560589fe3c2172',
    'Taiko': '0x2598d7bc9d3b4b6124f3282e49eee68db270f516',
    'Base': '0x13e46b2a3f8512ed4682a8fb8b560589fe3c2172',
    'Linea': '0x13e46b2a3f8512ed4682a8fb8b560589fe3c2172',
    'Mantle': '0x13e46b2a3f8512ed4682a8fb8b560589fe3c2172',
    'OpBNB': '0x13e46b2a3f8512ed4682a8fb8b560589fe3c2172',
    'Zora': '0x2598d7bc9d3b4b6124f3282e49eee68db270f516',
    'Manta': '0x13e46b2a3f8512ed4682a8fb8b560589fe3c2172',
    'Kroma': '0x13e46b2a3f8512ed4682a8fb8b560589fe3c2172',
    'ZKFair': '0x13e46b2a3f8512ed4682a8fb8b560589fe3c2172',
    'Blast': '0x13e46b2a3f8512ed4682a8fb8b560589fe3c2172',
    'ZetaChain': '0x13e46b2a3f8512ed4682a8fb8b560589fe3c2172',
    'Mode': '0x13e46b2a3f8512ed4682a8fb8b560589fe3c2172',
    'Merlin': '0x4b8a4641c140b3aa6be8d99786fafe47a65869db',
    'BOB': '0x13e46b2a3f8512ed4682a8fb8b560589fe3c2172',
    'Bitlayer': '0x13e46b2a3f8512ed4682a8fb8b560589fe3c2172',
    'BounceBit': '0x13e46b2a3f8512ed4682a8fb8b560589fe3c2172',
    'Optopia': '0x13e46b2a3f8512ed4682a8fb8b560589fe3c2172',
    'Cyber': '0x13e46b2a3f8512ed4682a8fb8b560589fe3c2172',
    'Mint': '0x13e46b2a3f8512ed4682a8fb8b560589fe3c2172',
    'AlienxChain': '0x13e46b2a3f8512ed4682a8fb8b560589fe3c2172',
}


abi_orbiter = [
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "Transfer",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "bytes",
                "name": "data",
                "type": "bytes"
            }
        ],
        "name": "transfer",
        "outputs": [

        ],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "contract IERC20",
                "name": "token",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            },
            {
                "internalType": "bytes",
                "name": "data",
                "type": "bytes"
            }
        ],
        "name": "transferToken",
        "outputs": [

        ],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "contract IERC20",
                "name": "token",
                "type": "address"
            },
            {
                "internalType": "address[]",
                "name": "tos",
                "type": "address[]"
            },
            {
                "internalType": "uint256[]",
                "name": "values",
                "type": "uint256[]"
            }
        ],
        "name": "transferTokens",
        "outputs": [

        ],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address[]",
                "name": "tos",
                "type": "address[]"
            },
            {
                "internalType": "uint256[]",
                "name": "values",
                "type": "uint256[]"
            }
        ],
        "name": "transfers",
        "outputs": [

        ],
        "stateMutability": "payable",
        "type": "function"
    }
]