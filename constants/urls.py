# URLS

import os


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
        "eth-sepolia": "https://sepolia.etherscan.io/address/"

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
        "base-sepolia": f"https://lb.drpc.org/ogrpc?network=base-sepolia&dkey={os.getenv('DRPC_API_KEY')}"
    }
    return map.get(chain)


def XCHANGE_BUY(chain_id, token1):
    return f"https://x7finance.org/swap?chainId={chain_id}&token1={token1}"


def UNISWAP_BUY(chain_id, token1):
    return f"https://app.uniswap.org/swap?outputCurrency={token1}"



# TG
TG_MAIN = "t.me/x7portal"
TG_ALERTS = "t.me/xchange_alerts"
TG_ANNOUNCEMENTS = "t.me/x7announcements"
TG_DAO = "https://telegram.me/collablandbot?start=VFBDI1RFTCNDT01NIy0xMDAyMTM5MTc4NTQx"


# LINKS
CA_DIRECTORY = "https://www.x7finance.org/en/docs/breakdowns/contracts"
DISCORD = "https://discord.gg/x7finance"
DUNE = "https://dune.com/mike_x7f/x7finance"
GITHUB = "https://github.com/x7finance/"
MEDIUM = "https://medium.com/@X7Finance"
PIONEERS = "https://img.x7.finance/pioneers/"
REDDIT = "https://www.reddit.com/r/x7finance"
SNAPSHOT = "https://snapshot.org/#/x7finance.eth"
TWITTER = "https://twitter.com/x7_finance/"
WARPCAST = "https://warpcast.com/x7finance"
WP_LINK = "https://x7.finance/wp/v1_1_0/X7FinanceWhitepaper.pdf"
XCHANGE = "https://x7finance.org/"