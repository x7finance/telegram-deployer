# SMART CA

def DEPLOYER(chain):
    if chain == "base-sepolia":
        return "0x507c527379ebe223fb1e5ac4b750123ad88c68ee"
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
    if chain == "eth":
        if loan_id is not None and loan_id < 21:
            return "0x740015c39da5d148fca25a467399d00bce10c001"
        else:
            return "0x74001DcFf64643B76cE4919af4DcD83da6Fe1E02"
    else:
        return "0x740015c39da5d148fca25a467399d00bce10c001"

def LPOOL_RESERVE(chain):
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

def ILL001(chain):
    if chain == "base":
        return "0x7400165E167479a3c81C8fC8CC3df3D2a92E9017"
    else:
        return "0x7400165E167479a3c81C8fC8CC3df3D2a92E9017"
    
def ILL003(chain):
    if chain == "base":
        return "0x74001C747B6cc9091EE63bC9424DfF633FBAc617"
    else:
        return "0x74001C747B6cc9091EE63bC9424DfF633FBAc617"
    
def ILL004(chain):
    if chain == "base":
        return "0xF9832C813104a6256771dfBDd3a243D24B7D7941"
    else:
        return "0xF9832C813104a6256771dfBDd3a243D24B7D7941"

