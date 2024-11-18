# SMART CA

def DEPLOYER(chain):
    map = {
        "base": "0xfD392Fc17fcCe76b41d9ab4Ea72943bc5e244F6e",
        "base-sepolia": "0xfD440554a157783746fC8DDD482aD1C839088D18",
        "eth": "0xfD392Fc17fcCe76b41d9ab4Ea72943bc5e244F6e",
        "eth-sepolia": "0x7f36eB4a0C9279b2AcF88Bb1ED740b65c808F1bd"
    }
    return map.get(chain) 

def FACTORY(chain):
        return "0x8B76C05676D205563ffC1cbd11c0A6e3d83929c5"

def ILL004(chain):
    map = {
        "base": "0x3c0E49D9b72FdDAeF36e2962368b073Bc5A76481",
        "base-sepolia": "0xB4190B1b6FD00A9699b5FEa913e7D981318fef5a",
        "eth": "0x3c0E49D9b72FdDAeF36e2962368b073Bc5A76481",
        "eth-sepolia": "0xB4190B1b6FD00A9699b5FEa913e7D981318fef5a"
    }
    return map.get(chain) 

def ILL005(chain):
    map = {
        "base": "0x90482AD3aa56675ba313dAC14C3a7717bAD5B24D",
        "base-sepolia": "0xA78949b5f46aC0D92DCD6355745f2B9f9984a5b3",
        "eth": "0x90482AD3aa56675ba313dAC14C3a7717bAD5B24D",
        "eth-sepolia": "0xA78949b5f46aC0D92DCD6355745f2B9f9984a5b3"
    }
    return map.get(chain) 

def LPOOL(chain):
    map = {
        "base": "0x4eE199B7DFED6B96402623BdEcf2B1ae2f3750Dd",
        "base-sepolia": "0x0E2F369Fdc070521ae23A8BcB4Bad0310044a1e8",
        "eth": "0x74001DcFf64643B76cE4919af4DcD83da6Fe1E02",
        "eth-sepolia": "0xcad129C25D092a48bAC897CfbA887F16762E139f"
    }
    return map.get(chain)


DEAD = "0x000000000000000000000000000000000000dEaD"
ZERO = "0x0000000000000000000000000000000000000000"