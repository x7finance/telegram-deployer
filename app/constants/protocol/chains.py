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
        live=True,
        name="Base",
        short_name="base",
        scan_name="Basescan",
        id=8453,
        native="eth",
        address="0x4200000000000000000000000000000000000006",
        scan_token=urls.scan_url("base", "token"),
        scan_address=urls.scan_url("base", "address"),
        scan_tx=urls.scan_url("base", "tx"),
        dext="base",
        rpc_url=urls.RPC("base"),
    ),
    "eth": ChainInfo(
        live=True,
        name="ETH",
        short_name="eth",
        scan_name="Etherscan",
        id=1,
        native="eth",
        address="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        scan_token=urls.scan_url("eth", "token"),
        scan_address=urls.scan_url("eth", "address"),
        scan_tx=urls.scan_url("eth", "tx"),
        dext="ether",
        rpc_url=urls.rpc("eth"),
    ),
}

TESTNETS = {
    "base-sepolia": ChainInfo(
        live=True,
        name="Base Sepolia",
        short_name="base-testnet",
        scan_name="Base Sepolia Scan",
        id=84532,
        native="eth",
        address="0x4200000000000000000000000000000000000006",
        scan_token=urls.scan_url("base-sepolia", "token"),
        scan_address=urls.scan_url("base-sepolia", "address"),
        scan_tx=urls.scan_url("base-sepolia", "tx"),
        dext=None,
        rpc_url=urls.rpc("base-sepolia"),
    ),
    "eth-sepolia": ChainInfo(
        live=True,
        name="Eth Sepolia",
        short_name="eth-testnet",
        scan_name="Eth Sepolia Scan",
        id=11155111,
        native="eth",
        address="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        scan_token=urls.scan_url("eth-sepolia", "token"),
        scan_address=urls.scan_url("eth-sepolia", "address"),
        scan_tx=urls.scan_url("eth-sepolia", "tx"),
        dext=None,
        rpc_url=urls.rpc("eth-sepolia"),
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
