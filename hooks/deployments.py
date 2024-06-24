# LAUNCH

from constants import ca,  chains
from web3 import Web3
from hooks import api


def deploy_token(chain, name, symbol, supply, owner, address, key):
    if chain not in chains.chains:
        raise ValueError(f"Invalid chain: {chain}")
    
    w3 = Web3(Web3.HTTPProvider(chains.chains[chain].w3))
    contract_address = ca.DEPLOYER(chain)
    contract_abi = api.ChainScan().get_abi(contract_address, chain)
    
    contract = w3.eth.contract(
        address=w3.to_checksum_address(contract_address),
        abi=contract_abi
    )

    try:
        gas_estimate = contract.functions.deployToken(name, symbol, int(supply), owner).estimate_gas({
            'from': address
        })
        
        gas_price = w3.eth.gas_price
        
        transaction = contract.functions.deployToken(name, symbol, int(supply), owner).build_transaction({
            'from': address,
            'nonce': w3.eth.get_transaction_count(address),
            'gasPrice': gas_price,
            'gas': gas_estimate,
        })

        signed_txn = w3.eth.account.sign_transaction(transaction, key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        logs = contract.events.TokenDeployed().process_receipt(tx_receipt)
        
        return logs[0]['args']['tokenAddress']

    except Exception as e:
        return f'Error deploying token: {e}'
    

def create_pair(chain, token1, token2, address, key):
    if chain not in chains.chains:
        raise ValueError(f"Invalid chain: {chain}")

    w3 = Web3(Web3.HTTPProvider(chains.chains[chain].w3))
    contract_address = ca.FACTORY(chain)
    contract_abi = api.ChainScan().get_abi(contract_address, chain)
    contract = w3.eth.contract(
        address=w3.to_checksum_address(contract_address),
        abi=contract_abi
    )

    try:
        transaction = contract.functions.createPair(token1, token2).build_transaction({
            'from': address,
            'nonce': w3.eth.get_transaction_count(address),
            'gasPrice': w3.eth.gas_price
        })

        gas_estimate = w3.eth.estimate_gas(transaction)
        transaction['gas'] = gas_estimate
        signed_txn = w3.eth.account.sign_transaction(transaction, key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        logs = contract.events.PairCreated().process_receipt(tx_receipt)
        return logs[0]['args']['pair']

    
    except Exception as e:
        return f'Error creating pair: {e}'


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
        buffer = 50000000000
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
       
        return {tx_hash.hex()}

    except Exception as e:
        return f'Error transferring balance: {e}'