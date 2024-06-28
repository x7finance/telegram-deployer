# CHAINS

import os
from constants import urls


class ChainInfo:
    def __init__(
        self,
        live: bool,
        name: str,
        scan_name: str,
        id: str,
        token: str,
        address: str,
        scan_token: str,
        scan_address: str,
        scan_tx: str,
        dext: str,
        w3: str,
        w3_fallback: str,
        api: str,
        key: str,
    ):
        self.live = live
        self.name = name
        self.scan_name = scan_name
        self.id = id
        self.token = token
        self.address = address
        self.scan_token = scan_token
        self.scan_address = scan_address
        self.scan_tx = scan_tx
        self.dext = dext
        self.w3 = w3
        self.w3_fallback = w3_fallback
        self.api = api
        self.key = key


chains = {
    "base-sepolia": ChainInfo(
        True,
        "Base Sepolia",
        "Base Sepolia Scan",
        "84532",
        "eth",
        "0x4200000000000000000000000000000000000006",
        urls.BASE_SEPOLIA_TOKEN,
        urls.BASE_SEPOLIA_ADDRESS,
        urls.BASE_SEPOLIA_TX,
        "ether",
        urls.BASE_SEPOLIA_RPC,
        urls.BASE_SEPOLIA_RPC_FALLBACK,
        urls.BASE_SEPOLIA_API,
        os.getenv('BASE'),
    ),
    "eth": ChainInfo(
        False,
        "ETH",
        "Etherscan",
        "1",
        "eth",
        "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        urls.ETHER_TOKEN,
        urls.ETHER_ADDRESS,
        urls.ETHER_TX,
        "ether",
        urls.ETH_RPC,
        urls.ETH_RPC_FALLBACK,
        urls.ETHER_API,
        os.getenv('ETHER'),
    ),
    "base": ChainInfo(
        False,
        "Base",
        "Basescan",
        "8453",
        "eth",
        "0x4200000000000000000000000000000000000006",
        urls.BASE_TOKEN,
        urls.BASE_ADDRESS,
        urls.BASE_TX,
        "base",
        urls.BASE_RPC,
        urls.BASE_RPC_FALLBACK,
        urls.BASE_API,
        os.getenv('BASE')
    ),
    "bsc": ChainInfo(
        False,
        "BSC",
        "BSCscan",
        "56",
        "bnb",
        "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",
        urls.BSC_TOKEN,
        urls.BSC_ADDRESS,
        urls.BSC_TX,
        "bsc",
        urls.BSC_RPC,
        urls.BSC_RPC_FALLBACK,
        urls.BSC_API,
        os.getenv('BSC')
    ),
    "arbitrum": ChainInfo(
        False,
        "Arbitrum",
        "Arbiscan",
        "42161",
        "eth",
        "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
        urls.ARB_TOKEN,
        urls.ARB_ADDRESS,
        urls.ARB_TX,
        "arbitrum",
        urls.ARB_RPC,
        urls.ARB_RPC_FALLBACK,
        urls.ARB_API,
        os.getenv('ARB')
    ),
    "optimism": ChainInfo(
        False,
        "Optimism",
        "Optimisticscan",
        "10",
        "eth",
        "0x4200000000000000000000000000000000000006",
        urls.OP_TOKEN,
        urls.OP_ADDRESS,
        urls.OP_TX,
        "optimism",
        urls.OP_RPC,
        urls.OP_RPC_FALLBACK,
        urls.OP_API,
        os.getenv('OP')
    ),
    "polygon": ChainInfo(
        False,
        "Polygon",
        "Polygonscan",
        "137",
        "matic",
        "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270",
        urls.POLY_TOKEN,
        urls.POLY_ADDRESS,
        urls.POLY_TX,
        "polygon",
        urls.POLY_RPC,
        urls.POLY_RPC_FALLBACK,
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
