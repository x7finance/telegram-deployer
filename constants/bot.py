from constants import ca

ADMINS = [1667971437]
BOT_NAME = "Xchange Create"

LIQUIDATION_DEPOSIT = 0.001
LIVE_LOAN = "005"
MAX_LOAN_AMOUNT = 5
MIN_LOAN_AMOUNT = 0.1
MAX_LOAN_LENGTH = 30

LOANS = {
    "004": {
        "origination_fee": lambda loan_in_wei: loan_in_wei * 2 // 100,
        "cost_string": "2% of borrowed capital",
        "contract": lambda chain: ca.ILL004(chain)
    },
    "005": {
        "origination_fee": lambda loan_in_wei: loan_in_wei + 10000000000000000,
        "cost_string": lambda chain_native: f"0.01 {chain_native.upper()}",
        "contract": lambda chain: ca.ILL005(chain)
    }
}