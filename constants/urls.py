# URLS

import os


# TG
TG_MAIN = "t.me/x7m105portal"
TG_ALERTS = "t.me/xchange_alerts"
TG_ANNOUNCEMENTS = "t.me/x7announcements"
TG_DAO = "https://telegram.me/collablandbot?start=VFBDI1RFTCNDT01NIy0xMDAyMTM5MTc4NTQx"


# ETHERSCAN
ETHER_API = "https://api.etherscan.io/api"
ETHER_TOKEN = "https://etherscan.io/token/"
ETHER_ADDRESS = "https://etherscan.io/address/"
ETHER_TX = "https://etherscan.io/tx/"
ETHER_GAS = "https://etherscan.io/gastracker/"


# BSCSCAN
BSC_API =  "https://api.bscscan.com/api"
BSC_TOKEN = "https://bscscan.com/token/"
BSC_ADDRESS = "https://bscscan.com/address/"
BSC_TX = "https://bscscan.com/tx/"
BSC_GAS = "https://bscscan.com/gastracker/"


# POLYGONSCAN
POLY_API = "https://api.polygonscan.com/api"
POLY_TOKEN = "https://polygonscan.com/token/"
POLY_ADDRESS = "https://polygonscan.com/address/"
POLY_TX = "https://polygonscan.com/tx/"
POLY_GAS = "https://polygonscan.com/gastracker/"


# ARBISCAN
ARB_API = "https://api.arbiscan.io/api"
ARB_TOKEN = "https://arbiscan.io/token/"
ARB_ADDRESS = "https://arbiscan.io/address/"
ARB_TX = "https://arbiscan.io/tx/"


# OPTIMISTIC
OP_API = "https://api-optimistic.etherscan.io/api"
OP_TOKEN = "https://optimistic.etherscan.io/token/"
OP_ADDRESS = "https://optimistic.etherscan.io/address/"
OP_TX = "https://optimistic.etherscan.io/tx/"


# BASESCAN
BASE_API = "https://api.basescan.org/api"
BASE_TOKEN = "https://basescan.org/token/"
BASE_ADDRESS = "https://basescan.org/address/"
BASE_TX = "https://basescan.org/tx/"

# BASESEPOLICASCAN
BASE_SEPOLIA_API = "https://api-sepolia.basescan.org/api"
BASE_SEPOLIA_TOKEN = "https://sepolia.basescan.org/token/"
BASE_SEPOLIA_ADDRESS = "https://sepolia.basescan.org/address/"
BASE_SEPOLIA_TX = "https://sepolia.basescan.org/tx/"

# DEXTOOLS
def DEX_TOOLS(chain):
    return f"https://www.dextools.io/app/{chain}/pair-explorer/"


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


# XCHANGE
XCHANGE = "https://x7finance.org/"

XCHANGE_LOANS = "https://www.x7finance.org/dashboard/loans/"
XCHANGE_FUND = "https://x7finance.org/fund"

def XCHANGE_BUY(chain_id, token1):
    return f"https://x7finance.org/?chainId={chain_id}&token1={token1}"


# RPCS
ETH_RPC = f"https://lb.drpc.org/ogrpc?network=ethereum&dkey={os.getenv('DRPC_API_KEY')}"
BASE_RPC = f"https://lb.drpc.org/ogrpc?network=base&dkey={os.getenv('DRPC_API_KEY')}"
BSC_RPC = f"https://lb.drpc.org/ogrpc?network=bsc&dkey={os.getenv('DRPC_API_KEY')}"
ARB_RPC = f"https://lb.drpc.org/ogrpc?network=arbitrum&dkey={os.getenv('DRPC_API_KEY')}"
OP_RPC = f"https://lb.drpc.org/ogrpc?network=optimism&dkey={os.getenv('DRPC_API_KEY')}"
POLY_RPC = f"https://lb.drpc.org/ogrpc?network=polygon&dkey={os.getenv('DRPC_API_KEY')}"
BASE_SEPOLIA_RPC = f"https://lb.drpc.org/ogrpc?network=base-sepolia&dkey={os.getenv('DRPC_API_KEY')}"

ETH_RPC_FALLBACK = f"https://eth-mainnet.g.alchemy.com/v2/{os.getenv('ALCHEMY_API_KEY')}"
BSC_RPC_FALLBACK = f"https://bnb-mainnet.g.alchemy.com/v2/{os.getenv('ALCHEMY_API_KEY')}"
POLY_RPC_FALLBACK = f"https://polygon-mainnet.g.alchemy.com/v2/{os.getenv('ALCHEMY_API_KEY')}"
OP_RPC_FALLBACK = f"https://opt-mainnet.g.alchemy.com/v2/{os.getenv('ALCHEMY_API_KEY')}"
ARB_RPC_FALLBACK = f"https://arb-mainnet.g.alchemy.com/v2/{os.getenv('ALCHEMY_API_KEY')}"
BASE_RPC_FALLBACK = f"https://base-mainnet.g.alchemy.com/v2/{os.getenv('ALCHEMY_API_KEY')}"
BASE_SEPOLIA_RPC_FALLBACK = f"https://base-sepolia.g.alchemy.com/v2/{os.getenv('ALCHEMY_API_KEY')}"