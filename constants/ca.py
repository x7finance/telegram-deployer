# SMART CA

def BURNER(chain):
    if chain == "base":
        return "0x70008F0B06060A31515733DB6dCB515c64f3DeAd"
    else:
        return "0x70008F0B06060A31515733DB6dCB515c64f3DeAd"
    
def DEFAULT_TOKEN_LIST(chain):
    if chain  == "base":
        return "0x7deF192aDB727777c5f24c05018cfbaFDFaD805a"
    else:
        return "0x7deF192aDB727777c5f24c05018cfbaFDFaD805a"

def DISCOUNT_ROUTER(chain):
    if chain == "base":
        return "0x7de8dd6146aa8b4a2ed8343aa83bc8874fb17000"
    else:
        return "0x7de8dd6146aa8b4a2ed8343aa83bc8874fb17000"

def ECO_SPLITTER(chain):
    if chain == "base":
        return "0x70001BA1BA4d85739E7B6A7C646B8aba5ed6c888"
    else:
        return "0x70001BA1BA4d85739E7B6A7C646B8aba5ed6c888"

def FACTORY(chain):
    if chain == "base":
        return "0x7de800467aFcE442019884f51A4A1B9143a34fAc"
    else:
        return "0x7de800467aFcE442019884f51A4A1B9143a34fAc"

def FEE_TO(chain):
    if chain == "eth" or chain == "base":
        return "0x7000E84aF80f817010cF1A9C0d5f8Df2A5DA60DD"
    else:
        return "0x7000E84aF80f817010cF1A9C0d5f8Df2A5DA60DD"

def LENDING_DISCOUNT(chain):
    if chain == "base":
        return "0x74001e463b3c7dc95d96a1fdbe621678c24d47da"
    else:
        return "0x74001e463b3c7dc95d96a1fdbe621678c24d47da"

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
    
def PROFIT_SHARING(chain):
    if chain == "base":
        return "0x700008707507005e5673b644ecb2387673941000"
    else:
        return "0x700008707507005e5673b644ecb2387673941000"

def ROUTER(chain):
    if chain == "base":
        return "0x7DE8063E9fB43321d2100e8Ddae5167F56A50060"
    else:
        return "0x7DE8063E9fB43321d2100e8Ddae5167F56A50060"

def TIME_LOCK(chain):
    if chain == "base":
        return "0x7000F4Cddca46FB77196466C3833Be4E89ab810C"
    else:
        return "0x7000F4Cddca46FB77196466C3833Be4E89ab810C"
    
def TREASURY_SPLITTER(chain):
    if chain == "base":
        return "0x7000706E2727686eDF46cA0E42690F87b9de1999"
    else:
        return "0x70006B785AA87821331a974C3d5af81CdE5BB999"

def X7100_DISCOUNT(chain):
    if chain == "base":
        return "0x7100AAcC6047281b105201cb9e0DEcF9Ae5431DA"
    else:
        return "0x7100AAcC6047281b105201cb9e0DEcF9Ae5431DA"
    
def X7100_LIQ_HUB(chain):
    if chain == "base":
        return "0x27a24a9a1Ee636E0C675964185e1f13545bA8605"
    else:
        return "0x27a24a9a1Ee636E0C675964185e1f13545bA8605"
    
def X7DAO_DISCOUNT(chain):
    if chain == "base":
        return "0x7da05D75f51056f3B83b43F397668Cf6A5051cDa"
    else:
        return "0x7da05D75f51056f3B83b43F397668Cf6A5051cDa"
    
def X7DAO_LIQ_HUB(chain):
    if chain == "base":
        return "0xB06D584a30225A05583905C599a7A9990FEF062b"
    else:
        return "0xB06D584a30225A05583905C599a7A9990FEF062b"
    
def X7R_DISCOUNT(chain):
    if chain == "base":
        return "0x712bC6ddcd97A776B2482531058C629456B93eda"
    else:
        return "0x712bC6ddcd97A776B2482531058C629456B93eda"
    
def X7R_LIQ_HUB(chain):
    if chain == "base":
        return "0x734B81d7De2b8D85eb71E5c7548f5f8D220a7782"
    else:
        return "0x734B81d7De2b8D85eb71E5c7548f5f8D220a7782"

def XCHANGE_DISCOUNT(chain):
    if chain == "base":
        return "0x7de8ab0dd777561ce98b7ef413f6fd564e89c1da"
    else:
        return "0x7de8ab0dd777561ce98b7ef413f6fd564e89c1da"

def HUBS(chain):
    return {
    "x7r": X7R_LIQ_HUB(chain),
    "x7dao": X7DAO_LIQ_HUB(chain),
    "x7100": X7100_LIQ_HUB(chain),
}


# LOANS

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

