# SMART CA

def DEPLOYER(chain):
    map = {
        "base": "0xd9511408f0042b75D2Be3Bfe9d9e9df7624AFcc1",
        "base-sepolia": "0x8a9aE146e1771b56Ed2cd31853b3Dd355b9BFA03",
        "eth": "0x32149a5fc4974095217a2318ba0fD8D9A5fC10D2",
        "eth-sepolia": "0x09503d48Ac958AC40ed0E8Ab466D5a44190eC903"
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