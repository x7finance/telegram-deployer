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
        
        if logs:
            return logs[0]['args']['tokenAddress']
        else:
            return "0x"
        
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
        if logs:
            return logs[0]['args']['pair']
        else:
            return "0x"
    
    except Exception as e:
        return f'Error creating pair: {e}'
    

def add_liq(chain, eth, token, token_amount, deadline, address, key):
    if chain not in chains.chains:
        raise ValueError(f"Invalid chain: {chain}")

    w3 = Web3(Web3.HTTPProvider(chains.chains[chain].w3))
    contract_address = ca.ROUTER(chain)
    contract_abi = api.ChainScan().get_abi(contract_address, chain)
    contract = w3.eth.contract(
        address=w3.to_checksum_address(contract_address),
        abi=contract_abi
    )

    try:
        token_address = w3.to_checksum_address(token)
        transaction = contract.functions.addLiquidityETH(
            token_address,
            int(token_amount),  # amountTokenDesired
            int(token_amount),  # amountTokenMin
            w3.to_wei(eth, 'ether'),    # amountETHMin
            w3.to_checksum_address(address),
            int(deadline)
        ).build_transaction({
            'from': address,
            'nonce': w3.eth.get_transaction_count(address),
            'gasPrice': w3.eth.gas_price,
            'value': w3.to_wei(eth, 'ether')  # Specify value to transfer in Wei
        })

        # Estimate gas and set gas limit
        gas_estimate = w3.eth.estimate_gas(transaction)
        transaction['gas'] = gas_estimate

        # Print transaction details for debugging
        print(f"Transaction details:\n{transaction}")

        # Sign transaction and send
        signed_txn = w3.eth.account.sign_transaction(transaction, key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        # Wait for transaction receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        # Check for logs in the transaction receipt
        logs = tx_receipt.logs
        if logs:
            return f"Liquidity added successfully. Logs: {logs}\nTransaction Hash: {tx_hash.hex()}"
        else:
            return "Liquidity added, but no logs found in the transaction receipt."
    
    except ValueError as ve:
        return f'ValueError: {ve}'
    except Exception as e:
        return f'Error adding liquidity: {e}'