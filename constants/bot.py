from constants import ca

BOT_NAME = "Xchange Launcher"
LOAN_DEPOSIT = 0.1
MAX_LOAN_AMOUNT = 5
ADMINS = [1667971437]

ACTIVE_LOAN_ADDRESS = "ILL004"

def ACTIVE_LOAN(chain, loan_amount = None):
    if ACTIVE_LOAN_ADDRESS == "ILL004":
        if loan_amount is not None:
            loan_in_wei = float(loan_amount) * 10 ** 18
            origination_fee = int(loan_in_wei) * 2 // 100
            loan_deposit = LOAN_DEPOSIT * 10 ** 18
            fee = origination_fee + loan_deposit
            return int(fee), ca.ILL004(chain)
    else:
            raise ValueError("Loan amount is required for ILL004")
    
    if ACTIVE_LOAN_ADDRESS == "ILL005":
        fee = LOAN_DEPOSIT + 0.01
        return fee, ca.ILL005(chain)
    
