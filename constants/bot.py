from constants import ca

ADMINS = [1667971437]
BOT_NAME = "Xchange Create"


def LIVE_LOAN(chain, return_type="both"):
    address = ca.ILL005(chain)
    name = "005"
    
    if return_type == "address":
        return address
    elif return_type == "name":
        return name
    else:
        return address, name

LIQUIDATION_DEPOSIT = 0.001
MAX_LOAN_AMOUNT = 5
MIN_LOAN_AMOUNT = 0.1
MAX_LOAN_LENGTH = 30