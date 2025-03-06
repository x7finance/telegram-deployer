import os


UNISWAP = "https://app.uniswap.org/"
XCHANGE = "https://x7finance.org/"


def scan_url(chain, category):
    map = {
        "eth": "https://etherscan.io/",
        "bsc": "https://bscscan.com/",
        "poly": "https://polygonscan.com/",
        "arb": "https://arbiscan.io/",
        "op": "https://optimistic.etherscan.io/",
        "base": "https://basescan.org/",
        "eth-sepolia": "https://sepolia.etherscan.io/",
        "base-sepolia": "https://sepolia.basescan.org/",
    }

    categories = {
        "address": "address/",
        "gas": "gastracker/",
        "token": "token/",
        "tx": "tx/",
    }

    base_url = map.get(chain)
    category_path = categories.get(category)

    return base_url + category_path


def dex_tools_link(chain, address):
    return f"https://www.dextools.io/app/{chain}/pair-explorer/{address}"


def rpc(chain):
    map = {
        "eth": f"https://lb.drpc.org/ogrpc?network=ethereum&dkey={os.getenv('DRPC_API_KEY')}",
        "eth-sepolia": f"https://lb.drpc.org/ogrpc?network=sepolia&dkey={os.getenv('DRPC_API_KEY')}",
        "base": f"https://lb.drpc.org/ogrpc?network=base&dkey={os.getenv('DRPC_API_KEY')}",
        "base-sepolia": f"https://lb.drpc.org/ogrpc?network=base-sepolia&dkey={os.getenv('DRPC_API_KEY')}",
    }
    return map.get(chain)


def xchange_buy(chain_id, token1):
    return f"https://x7finance.org/swap?chainId={chain_id}&token1={token1}"


def uniswap_buy(chain_id, token1):
    return f"https://app.uniswap.org/swap?outputCurrency={token1}"
