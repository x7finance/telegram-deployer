import os


UNISWAP = "https://app.uniswap.org/"
XCHANGE = "https://x7finance.org/"


def SCAN_API(chain):
    map = {
        "base": "https://api.basescan.org/api",
        "base-sepolia": "https://api-sepolia.basescan.org/api",
        "eth": "https://api.etherscan.io/api",
        "eth-sepolia": "https://api-sepolia.etherscan.io/api",
    }
    return map.get(chain)


def SCAN_TOKEN(chain):
    map = {
        "base": "https://basescan.org/token/",
        "base-sepolia": "https://sepolia.basescan.org/token/",
        "eth": "https://etherscan.io/token/",
        "eth-sepolia": "https://sepolia.etherscan.io/token/",
    }
    return map.get(chain)


def SCAN_ADDRESS(chain):
    map = {
        "base": "https://basescan.org/address/",
        "eth": "https://etherscan.io/address/",
        "base-sepolia": "https://sepolia.basescan.org/address/",
        "eth-sepolia": "https://sepolia.etherscan.io/address/",
    }
    return map.get(chain)


def SCAN_TX(chain):
    map = {
        "base": "https://basescan.org/tx/",
        "eth": "https://etherscan.io/tx/",
        "base-sepolia": "https://sepolia.basescan.org/tx/",
        "eth-sepolia": "https://sepolia.etherscan.io/tx/",
    }
    return map.get(chain)


def DEX_TOOLS(chain, address):
    return f"https://www.dextools.io/app/{chain}/pair-explorer/{address}"


def RPC(chain):
    map = {
        "eth": f"https://lb.drpc.org/ogrpc?network=ethereum&dkey={os.getenv('DRPC_API_KEY')}",
        "eth-sepolia": f"https://lb.drpc.org/ogrpc?network=sepolia&dkey={os.getenv('DRPC_API_KEY')}",
        "base": f"https://lb.drpc.org/ogrpc?network=base&dkey={os.getenv('DRPC_API_KEY')}",
        "base-sepolia": f"https://lb.drpc.org/ogrpc?network=base-sepolia&dkey={os.getenv('DRPC_API_KEY')}",
    }
    return map.get(chain)


def XCHANGE_BUY(chain_id, token1):
    return f"https://x7finance.org/swap?chainId={chain_id}&token1={token1}"


def UNISWAP_BUY(chain_id, token1):
    return f"https://app.uniswap.org/swap?outputCurrency={token1}"
