from web3 import AsyncWeb3

from constants.bot import urls
from utils import tools


class ChainInfo:
    def __init__(
        self,
        live: bool,
        name: str,
        short_name: str,
        scan_name: str,
        id: int,
        native: str,
        address: str,
        scan_token: str,
        scan_address: str,
        scan_tx: str,
        dext: str,
        rpc_url: str,
    ):
        self.live = live
        self.name = name
        self.short_name = short_name
        self.scan_name = scan_name
        self.id = id
        self.native = native
        self.address = address
        self.scan_token = scan_token
        self.scan_address = scan_address
        self.scan_tx = scan_tx
        self.dext = dext
        self.w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc_url))


MAINNETS = {
    "base": ChainInfo(
        True,
        "Base",
        "base",
        "Basescan",
        8453,
        "eth",
        "0x4200000000000000000000000000000000000006",
        urls.SCAN_TOKEN("base"),
        urls.SCAN_ADDRESS("base"),
        urls.SCAN_TX("base"),
        "base",
        urls.RPC("base"),
    ),
    "eth": ChainInfo(
        True,
        "ETH",
        "eth",
        "Etherscan",
        1,
        "eth",
        "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        urls.SCAN_TOKEN("eth"),
        urls.SCAN_ADDRESS("eth"),
        urls.SCAN_TX("eth"),
        "ether",
        urls.RPC("eth"),
    ),
}

TESTNETS = {
    "base-sepolia": ChainInfo(
        True,
        "Base Sepolia",
        "base-testnet",
        "Base Sepolia Scan",
        84532,
        "eth",
        "0x4200000000000000000000000000000000000006",
        urls.SCAN_TOKEN("base-sepolia"),
        urls.SCAN_ADDRESS("base-sepolia"),
        urls.SCAN_TX("base-sepolia"),
        "ether",
        urls.RPC("base-sepolia"),
    ),
    "eth-sepolia": ChainInfo(
        True,
        "Eth Sepolia",
        "eth-testnet",
        "Eth Sepolia Scan",
        11155111,
        "eth",
        "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        urls.SCAN_TOKEN("eth-sepolia"),
        urls.SCAN_ADDRESS("eth-sepolia"),
        urls.SCAN_TX("eth-sepolia"),
        "ether",
        urls.RPC("eth-sepolia"),
    ),
}


class DexInfo:
    def __init__(self, url: str, liq_link: str):
        self.url = url
        self.liq_link = liq_link


DEXES = {
    "xchange": DexInfo(urls.XCHANGE, "liquidity"),
    "uniswap": DexInfo(urls.UNISWAP, "positions"),
}


async def get_active_chains():
    if tools.is_local():
        return {**MAINNETS, **TESTNETS}
    return {**MAINNETS}


async def get_chain_info(chain):
    active_chains = await get_active_chains()
    if chain in active_chains:
        chain_info = active_chains[chain]
        return chain_info


async def get_full_names():
    active_chains = await get_active_chains()
    chain_names = [chain.name for chain in active_chains.values()]
    return "\n".join(chain_names)


async def get_short_names():
    active_chains = await get_active_chains()
    chain_list = [key.upper() for key in active_chains.keys()]
    return "\n".join(chain_list)
