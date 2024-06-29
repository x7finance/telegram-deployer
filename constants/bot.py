from web3 import Web3

from constants import ca, chains

BOT_NAME = "Xchange Create"
LOAN_DEPOSIT = 0.1
MAX_LOAN_AMOUNT = 5
MIN_LOAN_AMOUNT = 0.5
ADMINS = [1667971437]

ACTIVE_LOAN_ADDRESS = "ILL004"

def ACTIVE_LOAN(chain, loan_amount):
    chain_native = chains.chains[chain].token
    chain_web3 = chains.chains[chain].w3
    web3 = Web3(Web3.HTTPProvider(chain_web3))
    if ACTIVE_LOAN_ADDRESS == "ILL004":
        loan_in_wei = web3.to_wei(loan_amount, 'ether')
        origination_fee = loan_in_wei * 2 // 100
        loan_deposit = web3.to_wei(LOAN_DEPOSIT, 'ether')
        fee = origination_fee + loan_deposit
        text = f"Borrow upto {MAX_LOAN_AMOUNT} {chain_native.upper()} liquidity for {LOAN_DEPOSIT} {chain_native.upper()} + 2% of borrowed capital"
        return fee, ca.ILL004(chain), text
    
    if ACTIVE_LOAN_ADDRESS == "ILL005":
        fee = web3.to_wei(LOAN_DEPOSIT + 0.01, 'ether')
        text = f"Borrow upto {MAX_LOAN_AMOUNT} {chain_native.upper()} for 0.01 {chain_native.upper()}"
        return fee, ca.ILL005(chain), text
    
