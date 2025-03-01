from constants.protocol import addresses


ADMINS = [1667971437]
BOT_NAME = "Xchange Create"


def live_loan(chain, return_type="both"):
    address = addresses.ill005(chain)
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
