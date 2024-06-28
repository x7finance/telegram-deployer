from constants import ca

BOT_NAME = "Xchange Launcher"
LOAN_DEPOSIT = 0.1
MAX_LOAN_AMOUNT = 5
MIN_LOAN_AMOUNT = 0.5
ADMINS = [1667971437]

ACTIVE_LOAN_ADDRESS = "ILL004"

def ACTIVE_LOAN(chain, loan_amount):
    if ACTIVE_LOAN_ADDRESS == "ILL004":
        loan_in_wei = float(loan_amount) * 10 ** 18
        origination_fee = int(loan_in_wei) * 2 // 100
        loan_deposit = LOAN_DEPOSIT * 10 ** 18
        fee = origination_fee + loan_deposit
        text = f"Borrow upto {MAX_LOAN_AMOUNT} ETH liquidity for {LOAN_DEPOSIT} ETH + 2% of borrowed capital"
        return int(fee), ca.ILL004(chain), text
    
    if ACTIVE_LOAN_ADDRESS == "ILL005":
        fee = LOAN_DEPOSIT + 0.01
        text = f"Borrow upto {MAX_LOAN_AMOUNT} ETH liquidity for 0.01 ETH"
        return int(fee), ca.ILL005(chain), text
    
