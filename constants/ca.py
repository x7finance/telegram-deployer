# SMART CA

def DEPLOYER(chain):
    map = {
        "base": "0xf4C0124b9a862a281379374e3CCc564acC68a5af",
        "base-sepolia": "0x9a6570e285c4625339c621E9022dD3ef17376B33",
        "eth": "0xfD392Fc17fcCe76b41d9ab4Ea72943bc5e244F6e",
        "eth-sepolia": "0x38223487360226Cb25Ba8037b121e54D80A2e904"
    }
    return map.get(chain)


def DEPLOYER_UNISWAP(chain):
    map = {
        "base": "0xA33C9a350BE602957104486f95352B9589E85E15",
        "base-sepolia": "0x9a6570e285c4625339c621E9022dD3ef17376B33",
        "eth": "0xfD392Fc17fcCe76b41d9ab4Ea72943bc5e244F6e",
        "eth-sepolia": "0x38223487360226Cb25Ba8037b121e54D80A2e904"
    }
    return map.get(chain) 


def FACTORY(chain):
        return "0x8B76C05676D205563ffC1cbd11c0A6e3d83929c5"

def FACTORY_UNISWAP(chain):
    map = {
        "base": "0x8909Dc15e40173Ff4699343b6eB8132c65e18eC6",
        "base-sepolia": "0x9a6570e285c4625339c621E9022dD3ef17376B33",
        "eth": "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f",
        "eth-sepolia": "0xF62c03E08ada871A0bEb309762E260a7a6a880E6"
    }
    return map.get(chain) 

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
        "base-sepolia": "0x97dD34dF320CC490A071b794756423e2bE7D4B3b",
        "eth": "0x90482AD3aa56675ba313dAC14C3a7717bAD5B24D",
        "eth-sepolia": "0x97dD34dF320CC490A071b794756423e2bE7D4B3b"
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