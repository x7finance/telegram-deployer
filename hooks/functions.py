from telegram import *
from telegram.ext import *

from constants import ca, chains
from web3 import Web3
from hooks import api, tools


def deploy_token_without_loan(chain, name, symbol, supply, percent, owner, slippage, address, key, loan_fee):
    if chain not in chains.chains:
        raise ValueError(f"Invalid chain: {chain}")

    w3 = Web3(Web3.HTTPProvider(chains.chains[chain].w3))
    deployer_address = ca.DEPLOYER(chain)
    factory_address = ca.FACTORY(chain)

    deployer_abi = api.ChainScan().get_abi(deployer_address, chain)
    factory_abi = api.ChainScan().get_abi(factory_address, chain)

    deployer_contract = w3.eth.contract(address=w3.to_checksum_address(deployer_address), abi=deployer_abi)
    factory_contract = w3.eth.contract(address=w3.to_checksum_address(factory_address), abi=factory_abi)

    deadline = tools.timestamp_deadline()
    gas_price = w3.eth.gas_price
    nonce = w3.eth.get_transaction_count(address)

    params = {
        "name": name,
        "symbol": symbol,
        "supply": int(supply),
        "teamTokens": int(percent),
        "newOwner": owner,
        "slippageTolerance": slippage,
        "deadline": deadline
    }

    try:
        gas_estimate = deployer_contract.functions.deployTokenWithoutLoan(params).estimate_gas({
            'from': address,
            'nonce': nonce,
            'gasPrice': gas_price,
            'value': loan_fee
        })

        transaction = deployer_contract.functions.deployTokenWithoutLoan(params).build_transaction({
            'from': address,
            'nonce': nonce,
            'gasPrice': gas_price,
            'gas': gas_estimate,
            'value': loan_fee
        })

        signed_txn = w3.eth.account.sign_transaction(transaction, key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        create_log = deployer_contract.events.TokenDeployed().process_receipt(tx_receipt)
        pair_log = factory_contract.events.PairCreated().process_receipt(tx_receipt)
        return create_log[0]['args']['tokenAddress'], pair_log[0]['args']['pair']

    except Exception as e:
        return f'Error deploying token: {str(e)}'


def deploy_token_with_loan(chain, name, symbol, supply, percent, loan_amount, duration, owner, address, key, loan_fee):
    if chain not in chains.chains:
        raise ValueError(f"Invalid chain: {chain}")
    
    _, loan_contract, _ = tools.generate_loan_terms(chain, loan_amount)

    w3 = Web3(Web3.HTTPProvider(chains.chains[chain].w3))
    deployer_address = ca.DEPLOYER(chain)
    factory_address = ca.FACTORY(chain)

    deployer_abi = api.ChainScan().get_abi(deployer_address, chain)
    factory_abi = api.ChainScan().get_abi(factory_address, chain)

    deployer_contract = w3.eth.contract(address=w3.to_checksum_address(deployer_address), abi=deployer_abi)
    factory_contract = w3.eth.contract(address=w3.to_checksum_address(factory_address), abi=factory_abi)

    deadline = tools.timestamp_deadline()
    gas_price = w3.eth.gas_price
    nonce = w3.eth.get_transaction_count(address)

    params = {
        "name": name,
        "symbol": symbol,
        "supply": int(supply),
        "teamTokens": int(percent),
        "newOwner": owner,
        "loanTermContract": loan_contract,
        "loanAmount": int(loan_amount),
        "loanDurationSeconds": int(duration),
        "liquidityReceiver": owner,
        "deadline": deadline
    }

    try:
        gas_estimate = deployer_contract.functions.deployTokenWithLoan(params).estimate_gas({
            'from': address,
            'nonce': nonce,
            'gasPrice': gas_price,
            'value': loan_fee
        })

        transaction = deployer_contract.functions.deployTokenWithLoan(params).build_transaction({
            'from': address,
            'nonce': nonce,
            'gasPrice': gas_price,
            'gas': gas_estimate,
            'value': loan_fee
        })

        signed_txn = w3.eth.account.sign_transaction(transaction, key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        create_log = deployer_contract.events.TokenDeployed().process_receipt(tx_receipt)
        pair_log = factory_contract.events.PairCreated().process_receipt(tx_receipt)
        return create_log[0]['args']['tokenAddress'], pair_log[0]['args']['pair'], create_log[0]['args']['loanID']

    except Exception as e:
        return f'Error deploying token: {str(e)}'


def estimate_gas_without_loan(chain, name, symbol, supply, percent, owner, slippage, loan_fee):
    try:
        chain_web3 = chains.chains[chain].w3
        web3 = Web3(Web3.HTTPProvider(chain_web3))
        deployer_address = ca.DEPLOYER(chain)
        deployer_abi = api.ChainScan().get_abi(deployer_address, chain)
        deployer_contract = web3.eth.contract(address=web3.to_checksum_address(deployer_address), abi=deployer_abi)
        deadline = tools.timestamp_deadline()
        gas_price = web3.eth.gas_price
        nonce = web3.eth.get_transaction_count(ca.DEAD)

        params = {
            "name": name,
            "symbol": symbol,
            "supply": int(supply),
            "teamTokens": int(percent),
            "newOwner": owner,
            "slippageTolerance": slippage,
            "deadline": deadline
        }

        gas_estimate = deployer_contract.functions.deployTokenWithoutLoan(params).estimate_gas({
            'from': ca.DEAD,
            'nonce': nonce,
            'gasPrice': gas_price,
            'value': int(loan_fee)
        })

        gas_cost = gas_estimate * gas_price
        return gas_cost
    except Exception as e:
            return f"Error estimating gas: {str(e)}"


def estimate_gas_with_loan(chain, name, symbol, supply, percent, loan_amount, duration, owner, loan_fee):
    try:
        chain_web3 = chains.chains[chain].w3
        web3 = Web3(Web3.HTTPProvider(chain_web3))
        deployer_address = ca.DEPLOYER(chain)
        deployer_abi = api.ChainScan().get_abi(deployer_address, chain)
        deployer_contract = web3.eth.contract(address=web3.to_checksum_address(deployer_address), abi=deployer_abi)
        deadline = tools.timestamp_deadline()
        gas_price = web3.eth.gas_price
        nonce = web3.eth.get_transaction_count(ca.DEAD)
        _, loan_contract, _ = tools.generate_loan_terms(chain, web3.to_wei(loan_amount, 'ether'))

        params = {
            "name": name,
            "symbol": symbol,
            "supply": int(supply),
            "teamTokens": int(percent),
            "newOwner": owner,
            "loanTermContract": loan_contract,
            "loanAmount": loan_amount,
            "loanDurationSeconds": duration,
            "liquidityReceiver": owner,
            "deadline": deadline
        }
        
        gas_estimate = deployer_contract.functions.deployTokenWithLoan(params).estimate_gas({
            'from': ca.DEAD,
            'nonce': nonce,
            'gasPrice': gas_price,
            'value': int(loan_fee)
        })

        gas_cost = gas_estimate * gas_price
        return gas_cost

    except Exception as e:
        return f"Error estimating gas: {str(e)}"


def get_pool_funds(chain):
    if chain not in chains.chains:
        raise ValueError(f"Invalid chain: {chain}")
    
    w3 = Web3(Web3.HTTPProvider(chains.chains[chain].w3))
    contract_abi = api.ChainScan().get_abi(ca.LPOOL(chain), chain)
    contract = w3.eth.contract(
        address=w3.to_checksum_address(ca.LPOOL(chain)),
        abi=contract_abi
    )
    
    try:
        function_name = 'availableCapital'
        function_call = getattr(contract.functions, function_name)
        result = function_call().call()
        
        return w3.from_wei(result, 'ether')
    
    except Exception as e:
        return f'Error reading contract: {e}'
    

def transfer_balance(chain, address, owner, key):
    if chain not in chains.chains:
        raise ValueError(f"Invalid chain: {chain}")

    w3 = Web3(Web3.HTTPProvider(chains.chains[chain].w3))
    chain_id = int(chains.chains[chain].id)

    try:
        checksum_address = w3.to_checksum_address(address)
        checksum_owner = w3.to_checksum_address(owner)
        balance_wei = w3.eth.get_balance(checksum_address)
        gas_price = w3.eth.gas_price
        nonce = w3.eth.get_transaction_count(checksum_address)
        sample_transaction = {
            'from': checksum_address,
            'to': checksum_owner,
            'gasPrice': gas_price,
            'value': balance_wei // 2,
        }

        gas_estimate = w3.eth.estimate_gas(sample_transaction)
        gas_cost = gas_price * gas_estimate
        buffer_wei = 10**15
        amount_to_transfer = balance_wei - gas_cost - buffer_wei
        transaction = {
            'from': checksum_address,
            'to': checksum_owner,
            'value': amount_to_transfer,
            'gas': gas_estimate,
            'gasPrice': gas_price,
            'nonce': nonce,
            'chainId': chain_id
        }

        signed_txn = w3.eth.account.sign_transaction(transaction, key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_hash.hex()

    except Exception as e:
        return f'Error transferring balance: {e}'
    