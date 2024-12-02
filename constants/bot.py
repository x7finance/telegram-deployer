from constants import ca

ADMINS = [1667971437]
BOT_NAME = "Xchange Create"

LIQUIDATION_DEPOSIT = 0.001
LIVE_LOAN = lambda chain: ca.ILL005(chain)
MAX_LOAN_AMOUNT = 5
MIN_LOAN_AMOUNT = 0.1
MAX_LOAN_LENGTH = 30