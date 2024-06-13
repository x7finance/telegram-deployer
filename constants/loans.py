# LOANS

import math
from constants import ca, chains


class LoanTerm:
    def __init__(
        self,
        ca,
        title,
        name,
        origination_fee,
        retention_fee,
        leverage,
        min_loan,
        max_loan,
        min_loan_duration,
        max_loan_duration,
    ):
        self.ca = ca
        self.title = title
        self.name = name
        self.origination_fee = origination_fee
        self.retention_fee = retention_fee
        self.leverage = leverage
        self.min_loan = min_loan
        self.max_loan = max_loan
        self.min_loan_duration = min_loan_duration
        self.max_loan_duration = max_loan_duration
        

    def generate_terms(self, chain):
        if chain in chains.CHAINS:
            chain_native = chains.CHAINS[chain].token
        return (
            f"\n{self.name}\n"
            f"> Loan Origination Fee: {self.origination_fee} ({self.leverage} leverage)\n"
            f"> Loan Retention Premium: {self.retention_fee}\n"
            f"> Min Loan: {self.min_loan} {chain_native.upper()}\n"
            f"> Max Loan: {self.max_loan} {chain_native.upper()}\n"
            f"> Min Loan Duration: {math.floor(self.min_loan_duration / 84600)} days\n"
            f"> Max Loan Duration: {math.floor(self.max_loan_duration / 84600)} days \n\n"
            f"> Principal Repayment Condition:\nPrincipal must be returned by the end of the loan term.\n\n"
            f"> Liquidation conditions:\nFailure to pay a premium payment by its due date or repay the principal by the end of the loan term will make the loan eligible for liquidation.\n\n")


def LOANS(chain): 
    return {
    "ill001": LoanTerm(
        ca.ILL001(chain),
        "X7 Initial Liquidity Loan (001) - X7ILL001",
        "Simple Loan",
        f"{2500 / 100}% of borrowed capital, payable within the transaction for adding initial liquidity",
        "0%",
        "4x",
        0.5,
        5,
        86400,
        2419200
    ),
    "ill003": LoanTerm(
        ca.ILL003(chain),
        "X7 Initial Liquidity Loan (003) - X7ILL003",
        "Interest Only Loan",
        f"{1500 / 100}% of borrowed capital",
        f"6.25% in premiums due by the end of each quarter of the loan term",
        "6.66x",
        0.5,
        5,
        86400,
        2419200
    ),
    "ill004": LoanTerm(
        ca.ILL004(chain),
        "X7 Initial Liquidity Loan (004) - X7ILL004",
        "Simple Loan",
        f"{200 / 100}% of borrowed capital",
        "0%",
        "50x",
        0.5,
        5,
        2419200,
        86400,
    ),
    "ill005": LoanTerm(
        ca.ILL001(chain),
        "X7 Initial Liquidity Loan (005) - X7ILL005",
        "Fixed Origination Fee",
        "0.01 ether",
        "0%",
        "100x",
        0.5,
        1,
        86400,
        2419200
    )
    
}

def loans_list(chain):
    loan_list = []
    for loan_key, loan_term in LOANS(chain).items():
        loan_list.append(f"{loan_key}")
    return ",".join(loan_list)


def OVERVIEW(chain):
    return (
    "*X7 Finance Loan Terms*\n\n"
    f"Use /loans {loans_list(chain)} for more details on individual loan contracts\n\n"
    "Loan terms are defined by standalone smart contracts that provide the following:\n\n"
    "1. Loan origination fee\n"
    "2. Loan retention premium fee schedule\n"
    "3. Principal repayment condition/maximum loan duration\n"
    "4. Liquidation conditions and Reward\n"
    "5. Loan duration\n\n"
    "The lending process delegates the loan terms to standalone smart contracts (see whitepaper below for "
    "more details). These loan terms contracts must be deployed, and then “added” or “removed” from the "
    "Lending Pool as “available” loan terms for new loans. The DAO will be able to add or remove these term "
    "contracts.\n\nLoan term contracts may be created by any interested third party, enabling a market "
    "process by which new loan terms may be invented, provided they implement the proper interface."
)
