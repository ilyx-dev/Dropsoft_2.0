import random

from w3.core.network.network import Network as Web3Network
from models.network import Network


def convert_to_web3_network(my_network: Network) -> Web3Network:
    rpc = random.choice(my_network.rpcs)
    return Web3Network(
        name=my_network.name,
        rpc=rpc,
        chain_id=my_network.chain_id,
        tx_type=my_network.tx_type
    )