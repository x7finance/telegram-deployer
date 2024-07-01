# SMART CA

def DEPLOYER(chain):
    if chain == "base-sepolia":
        return "0xF8BEdB23926b72338C4471E4916FA1e0925Bb6aB"
    if chain  == "base":
        return "0x47b95167B8cbe70Fffc1dCEE812e7C0388ACB81d"
    else:
        return "0x47b95167B8cbe70Fffc1dCEE812e7C0388ACB81d"

def FACTORY(chain):
    if chain == "base":
        return "0x7de800467aFcE442019884f51A4A1B9143a34fAc"
    if chain == "base-sepolia":
        return "0x659bb4214ae3808870da2fd84ac0fd5a7e1e20fc"
    else:
        return "0x7de800467aFcE442019884f51A4A1B9143a34fAc"

def LPOOL(chain, loan_id=None):
    if chain == "base-sepolia":
        return "0xB2996ee6b84E03D33c276cE4ca8d5e268fB29908"
    if chain == "eth":
        if loan_id is not None and loan_id < 21:
            return "0x740015c39da5d148fca25a467399d00bce10c001"
        else:
            return "0x74001DcFf64643B76cE4919af4DcD83da6Fe1E02"
    else:
        return "0x740015c39da5d148fca25a467399d00bce10c001"

def LPOOL_RESERVE(chain):
    if chain == "base-sepolia":
        return "0x8549Ccd56B35AF4FC3f8B8C5BA3dda52AfE4dcE8"
    if chain == "base":
        return "0x7Ca54e9Aa3128bF15f764fa0f0f93e72b5267000"
    else:
        return "0x7Ca54e9Aa3128bF15f764fa0f0f93e72b5267000"
    
def ROUTER(chain):
    if chain == "base-sepolia":
        return "0x3CE05D3e85B8e1486644Baf2cD890b8E4062BaCF"
    if chain == "base":
        return "0x7DE8063E9fB43321d2100e8Ddae5167F56A50060"
    else:
        return "0x7DE8063E9fB43321d2100e8Ddae5167F56A50060"

def ILL004(chain):
    if chain == "base-sepolia":
        return "0xd95f799276A8373F7F234A7F211DE9E3a0ae6639"
    if chain == "base":
        return "0xF9832C813104a6256771dfBDd3a243D24B7D7941"
    else:
        return "0xF9832C813104a6256771dfBDd3a243D24B7D7941"
    
def ILL005(chain):
    if chain == "base-sepolia":
        return "0xd95f799276A8373F7F234A7F211DE9E3a0ae6639"
    if chain == "base":
        return "0xF9832C813104a6256771dfBDd3a243D24B7D7941"
    else:
        return "0xF9832C813104a6256771dfBDd3a243D24B7D7941"

