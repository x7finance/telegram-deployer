# SMART CA

def DEPLOYER(chain):
    if chain == "base-sepolia":
        return "0xfD440554a157783746fC8DDD482aD1C839088D18"
    if chain  == "base":
        return "0xfd392fc17fcce76b41d9ab4ea72943bc5e244f6e"
    else:
        return "0x47b95167B8cbe70Fffc1dCEE812e7C0388ACB81d"

def FACTORY(chain):
    if chain == "base-sepolia":
        return "0x8B76C05676D205563ffC1cbd11c0A6e3d83929c5"
    else:
        return "0x7de800467aFcE442019884f51A4A1B9143a34fAc"


def LPOOL(chain, loan_id=None):
    if chain == "base-sepolia":
        return "0x0E2F369Fdc070521ae23A8BcB4Bad0310044a1e8"
    if chain == "eth":
        if loan_id is not None and loan_id < 21:
            return "0x740015c39da5d148fca25a467399d00bce10c001"
        else:
            return "0x74001DcFf64643B76cE4919af4DcD83da6Fe1E02"
    else:
        return "0x740015c39da5d148fca25a467399d00bce10c001"

def LPOOL_RESERVE(chain):
    if chain == "base-sepolia":
        return "0xbae3a19E9a4644a5bb98Af0eddD42533C38E3785"
    if chain == "base":
        return "0x7Ca54e9Aa3128bF15f764fa0f0f93e72b5267000"
    else:
        return "0x7Ca54e9Aa3128bF15f764fa0f0f93e72b5267000"
    
def ROUTER(chain):
    return "0xC2defaD879dC426F5747F2A5b067De070928AA50"

def ILL004(chain):
    if chain == "base-sepolia":
        return "0xB4190B1b6FD00A9699b5FEa913e7D981318fef5a"
    if chain == "base":
        return "0x3c0E49D9b72FdDAeF36e2962368b073Bc5A76481"
    else:
        return "0x3c0E49D9b72FdDAeF36e2962368b073Bc5A76481"
    