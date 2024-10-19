# CHAINS

import os
from constants import urls


class ChainInfo:
    def __init__(
        self,
        live: bool,
        name: str,
        scan_name: str,
        id: int,
        token: str,
        address: str,
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
        self.address = address
        self.scan_token = scan_token
        self.scan_address = scan_address
        self.scan_tx = scan_tx
        self.dext = dext
        self.w3 = w3
        self.api = api
        self.key = key


chains = {
    "base-sepolia": ChainInfo(
        True,
        "Base Sepolia",
        "Base Sepolia Scan",
        84532,
        "eth",
        "0x4200000000000000000000000000000000000006",
        urls.SCAN_TOKEN("base-sepolia"),
        urls.SCAN_ADDRESS("base-sepolia"),
        urls.SCAN_TX("base-sepolia"),
        "ether",
        urls.RPC("base-sepolia"),
        urls.SCAN_API("base-sepolia"),
        os.getenv('BASE'),
    ),
    "eth-sepolia": ChainInfo(
        True,
        "Eth Sepolia",
        "Eth Sepolia Scan",
        11155111,
        "eth",
        "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        urls.SCAN_TOKEN("eth-sepolia"),
        urls.SCAN_ADDRESS("eth-sepolia"),
        urls.SCAN_TX("eth-sepolia"),
        "ether",
        urls.RPC("eth-sepolia"),
        urls.SCAN_API("eth-sepolia"),
        os.getenv('ETHER'),
    ),
    "eth": ChainInfo(
        True,
        "ETH",
        "Etherscan",
        1,
        "eth",
        "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        urls.SCAN_TOKEN("eth"),
        urls.SCAN_ADDRESS("eth"),
        urls.SCAN_TX("eth"),
        "ether",
        urls.RPC("eth"),
        urls.SCAN_API("eth"),
        os.getenv('ETHER'),
    ),
    "base": ChainInfo(
        True,
        "Base",
        "Basescan",
        8453,
        "eth",
        "0x4200000000000000000000000000000000000006",
        urls.SCAN_TOKEN("base"),
        urls.SCAN_ADDRESS("base"),
        urls.SCAN_TX("base"),
        "base",
        urls.RPC("base"),
        urls.SCAN_API("base"),
        os.getenv('BASE'),
    ),
}


def full_names():
    chain_names = [chain.name for chain in chains.values()]
    return "\n".join(chain_names)


def short_names():
    chain_list = list(chains.keys())
    return "\n".join(chain_list)


live = {key: value for key, value in chains.items() if value.live}
live_list = "\n".join([key.upper() for key in live.keys()])
