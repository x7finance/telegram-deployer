# SMART CA

def DEPLOYER(chain):
    map = {
        "base": "0xfd392fc17fcce76b41d9ab4ea72943bc5e244f6e",
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

def LPOOL(chain):
    map = {
        "base": "0x740015c39da5D148fcA25A467399D00bcE10c001",
        "base-sepolia": "0x0E2F369Fdc070521ae23A8BcB4Bad0310044a1e8",
        "eth": "0x74001DcFf64643B76cE4919af4DcD83da6Fe1E02",
        "eth-sepolia": "0xcad129C25D092a48bAC897CfbA887F16762E139f"
    }
    return map.get(chain) 

def LPOOL_RESERVE(chain):
    map = {
        "base": "0x7Ca54e9Aa3128bF15f764fa0f0f93e72b5267000",
        "base-sepolia": "0xeEa4C68B1424cF566c2Ce7F4479fB6dbE79f53Fe",
        "eth": "0x7Ca54e9Aa3128bF15f764fa0f0f93e72b5267000",
        "eth-sepolia": "0xeEa4C68B1424cF566c2Ce7F4479fB6dbE79f53Fe"
    }
    return map.get(chain) 

    
def ROUTER(chain):
    map = {
        "base": "0xC2defaD879dC426F5747F2A5b067De070928AA50",
        "base-sepolia": "0xde472CFDC852c45FA8AC082A07662cA4846bD9A2",
        "eth": "0x6b5422D584943BC8Cd0E10e239d624c6fE90fbB8",
        "eth-sepolia": "0x05B5034BfDbd930a93283aa52A10D700454A7a47"
    }
    return map.get(chain) 


DEAD = "0x000000000000000000000000000000000000dEaD"
ZERO = "0x0000000000000000000000000000000000000000"