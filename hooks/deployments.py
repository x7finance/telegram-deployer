from telegram import *
from telegram.ext import *

from constants import bot, ca, chains
from web3 import Web3
from hooks import api


def deploy_token(chain, name, symbol, supply, loan_supply, loan_amount, owner, address, key):
    if chain not in chains.chains:
        raise ValueError(f"Invalid chain: {chain}")
    
    w3 = Web3(Web3.HTTPProvider(chains.chains[chain].w3))
    deployer_address = ca.DEPLOYER(chain)
    deployer_abi = api.ChainScan().get_abi(deployer_address, chain)
    
    deployer_contract = w3.eth.contract(
        address=w3.to_checksum_address(deployer_address),
        abi=deployer_abi
    )

    factory_address = ca.FACTORY(chain)
    factory_abi = api.ChainScan().get_abi(factory_address, chain)
    
    factory_contract = w3.eth.contract(
        address=w3.to_checksum_address(factory_address),
        abi=factory_abi
    )

    try:
        loan_fee = int(bot.LOAN_FEE * 10 ** 18)
        gas_estimate = deployer_contract.functions.deployToken(
            name,
            symbol,
            int(supply),
            int(loan_supply),
            owner,
            ca.ILL004(chain),
            int(loan_amount),
            bot.LOAN_LENGTH,
            owner,
            api.timestamp_deadline()
        ).estimate_gas({
            'from': address,
            'value': loan_fee
        })
        
        gas_price = w3.eth.gas_price
        
        transaction = deployer_contract.functions.deployToken(
            name,
            symbol,
            int(supply),
            int(loan_supply),
            owner,
            ca.ILL004(chain),
            int(loan_amount),
            bot.LOAN_LENGTH,
            owner,
            api.timestamp_deadline()
        ).build_transaction({
            'from': address,
            'nonce': w3.eth.get_transaction_count(address),
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
        return f'Error deploying token: {e}'

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
        sample_transaction = {
            'from': checksum_address,
            'to': checksum_owner,
            'value': 0,
            'gasPrice': gas_price,
            'nonce': w3.eth.get_transaction_count(checksum_address)
        }

        gas_estimate = w3.eth.estimate_gas(sample_transaction)
        gas_cost = gas_price * gas_estimate
        buffer = 100000000000
        amount_to_transfer = balance_wei - gas_cost - buffer

        transaction = {
            'from': checksum_address,
            'to': checksum_owner,
            'value': amount_to_transfer,
            'gas': gas_estimate,
            'gasPrice': gas_price,
            'nonce': w3.eth.get_transaction_count(checksum_address),
            'chainId': chain_id
        }

        signed_txn = w3.eth.account.sign_transaction(transaction, key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
       
        return tx_hash.hex()

    except Exception as e:
        return f'Error transferring balance: {e}'
    

def approve_tokens(chain, token_address, spender, amount, address, key):
    if chain not in chains.chains:
        raise ValueError(f"Invalid chain: {chain}")
    
    w3 = Web3(Web3.HTTPProvider(chains.chains[chain].w3))
    token_abi = api.ChainScan().get_abi(token_address, chain)
    token_contract = w3.eth.contract(
        address=w3.to_checksum_address(token_address),
        abi=token_abi
    )
    
    try:
        gas_estimate = token_contract.functions.approve(spender, amount).estimate_gas({
            'from': address
        })
        
        gas_price = w3.eth.gas_price
        transaction = token_contract.functions.approve(spender, amount).build_transaction({
            'from': address,
            'nonce': w3.eth.get_transaction_count(address),
            'gasPrice': gas_price,
            'gas': gas_estimate,
        })
        
        signed_txn = w3.eth.account.sign_transaction(transaction, key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        return tx_hash.hex()
    
    except Exception as e:
        return f'Error approving tokens: {e}'
    
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
       
        function_name = 'availableCapital'  # Example function name
        
        function_call = getattr(contract.functions, function_name)
        result = function_call().call()
        
        return result
    
    except Exception as e:
        return f'Error reading contract: {e}'
