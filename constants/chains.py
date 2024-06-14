# CHAINS

import os
from constants import ca, urls


class ChainInfo:
    def __init__(
        self,
        live: bool,
        name: str,
        scan_name: str,
        id: str,
        token: str,
        scan_token: str,
        scan_address: str,
        scan_tx: str,
        dext: str,
        w3: str,
        api: str,
        key: str,
    ):
        self.live = live
        self.name = name
        self.scan_name = scan_name
        self.id = id
        self.token = token
        self.scan_token = scan_token
        self.scan_address = scan_address
        self.scan_tx = scan_tx
        self.dext = dext
        self.w3 = w3
        self.api = api
        self.key = key


chains = {
    "eth": ChainInfo(
        True,
        "ETH",
        "Etherscan",
        "1",
        "eth",
        urls.ETHER_TOKEN,
        urls.ETHER_ADDRESS,
        urls.ETHER_TX,
        "ether",
        urls.ETH_RPC,
        urls.ETHER_API,
        os.getenv('ETHER'),
    ),
    "base": ChainInfo(
        True,
        "Base",
        "Basescan",
        "8453",
        "eth",
        urls.BASE_TOKEN,
        urls.BASE_ADDRESS,
        urls.BASE_TX,
        "base",
        urls.BASE_RPC,
        urls.BASE_API,
        os.getenv('BASE')
    ),
    "bsc": ChainInfo(
        False,
        "BSC",
        "BSCscan",
        "56",
        "bnb",
        urls.BSC_TOKEN,
        urls.BSC_ADDRESS,
        urls.BSC_TX,
        "bsc",
        urls.BSC_RPC,
        urls.BSC_API,
        os.getenv('BSC')
    ),
    "arb": ChainInfo(
        False,
        "Arbitrum",
        "Arbiscan",
        "42161",
        "eth",
        urls.ARB_TOKEN,
        urls.ARB_ADDRESS,
        urls.ARB_TX,
        "arbitrum",
        urls.ARB_RPC,
        urls.ARB_API,
        os.getenv('ARB')
    ),
    "op": ChainInfo(
        False,
        "Optimism",
        "Optimisticscan",
        "10",
        "eth",
        urls.OP_TOKEN,
        urls.OP_ADDRESS,
        urls.OP_TX,
        "optimism",
        urls.OP_RPC,
        urls.OP_API,
        os.getenv('OP')
    ),
    "polygon": ChainInfo(
        False,
        "Polygon",
        "Polygonscan",
        "137",
        "matic",
        urls.POLY_TOKEN,
        urls.POLY_ADDRESS,
        urls.POLY_TX,
        "polygon",
        urls.POLY_RPC,
        urls.POLY_API,
        os.getenv('POLY')
    )
}


def full_names():
    chain_names = [chain.name for chain in chains.values()]
    return "\n".join(chain_names)


def short_names():
    chain_list = list(chains.keys())
    return "\n".join(chain_list)


live = {key: value for key, value in chains.items() if value.live}
live_list = "\n".join([key.upper() for key in live.keys()])
