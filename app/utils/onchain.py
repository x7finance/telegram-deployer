from constants.protocol import addresses
from constants.bot import settings
from constants.protocol import abis, chains
from utils import tools
from services import get_dbmanager

db = get_dbmanager()


async def deploy_token_without_loan(
    chain,
    name,
    symbol,
    supply,
    percent,
    description,
    twitter,
    telegram,
    website,
    buy_tax,
    sell_tax,
    owner,
    address,
    key,
    loan_fee,
):
    chain_info = await chains.get_chain_info(chain)

    deployer_address = addresses.deployer(chain)
    factory_address = addresses.factory(chain)

    deployer_abi = abis.read("deployer")
    factory_abi = abis.read("factory")

    deployer_contract = chain_info.w3.eth.contract(
        address=chain_info.w3.to_checksum_address(deployer_address),
        abi=deployer_abi,
    )
    factory_contract = chain_info.w3.eth.contract(
        address=chain_info.w3.to_checksum_address(factory_address),
        abi=factory_abi,
    )

    deadline = tools.timestamp_deadline()
    gas_price = await chain_info.w3.eth.gas_price
    nonce = await chain_info.w3.eth.get_transaction_count(address)

    params = {
        "name": name,
        "symbol": symbol,
        "supply": int(supply),
        "teamTokens": int(percent),
        "newOwner": owner,
        "slippageTolerance": 1,
        "deadline": deadline,
        "description": description,
        "twitterLink": twitter,
        "telegramLink": telegram,
        "websiteLink": website,
        "tokenURI": "",
        "buyTax": int(buy_tax),
        "sellTax": int(sell_tax),
        "taxWallet": owner,
    }

    try:
        gas_estimate = (
            await deployer_contract.functions.deployTokenWithoutLoan(
                params
            ).estimate_gas(
                {
                    "from": address,
                    "nonce": nonce,
                    "gasPrice": gas_price,
                    "value": int(loan_fee),
                }
            )
        )

        transaction = await deployer_contract.functions.deployTokenWithoutLoan(
            params
        ).build_transaction(
            {
                "from": address,
                "nonce": nonce,
                "gasPrice": gas_price,
                "gas": gas_estimate,
                "value": int(loan_fee),
            }
        )

        signed_tx = chain_info.w3.eth.account.sign_transaction(
            transaction, key
        )
        tx_hash = await chain_info.w3.eth.send_raw_transaction(
            signed_tx.raw_transaction
        )

        receipt = await chain_info.w3.eth.wait_for_transaction_receipt(
            tx_hash, timeout=30
        )
        if receipt.status == 1:
            create_log = (
                deployer_contract.events.TokenDeployed().process_receipt(
                    receipt
                )
            )
            pair_log = factory_contract.events.PairCreated().process_receipt(
                receipt
            )
            return create_log[0]["args"]["tokenAddress"], pair_log[0]["args"][
                "pair"
            ]
        else:
            return "Error deploying token"

    except Exception as e:
        return f"Error deploying token: {str(e)}"


async def deploy_token_with_loan(
    chain,
    name,
    symbol,
    supply,
    percent,
    description,
    twitter,
    telegram,
    website,
    buy_tax,
    sell_tax,
    loan_amount,
    duration,
    owner,
    address,
    key,
    loan_fee,
):
    loan_contract = settings.live_loan(chain, "address")

    chain_info = await chains.get_chain_info(chain)
    deployer_address = addresses.deployer(chain)
    factory_address = addresses.factory(chain)

    deployer_abi = abis.read("deployer")
    factory_abi = abis.read("factory")

    deployer_contract = chain_info.w3.eth.contract(
        address=chain_info.w3.to_checksum_address(deployer_address),
        abi=deployer_abi,
    )
    factory_contract = chain_info.w3.eth.contract(
        address=chain_info.w3.to_checksum_address(factory_address),
        abi=factory_abi,
    )

    deadline = tools.timestamp_deadline()
    gas_price = await chain_info.w3.eth.gas_price
    nonce = await chain_info.w3.eth.get_transaction_count(address)

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
        "deadline": deadline,
        "description": description,
        "twitterLink": twitter,
        "telegramLink": telegram,
        "websiteLink": website,
        "tokenURI": "",
        "buyTax": int(buy_tax),
        "sellTax": int(sell_tax),
        "taxWallet": owner,
    }

    try:
        gas_estimate = await deployer_contract.functions.deployTokenWithLoan(
            params
        ).estimate_gas(
            {
                "from": address,
                "nonce": nonce,
                "gasPrice": gas_price,
                "value": int(loan_fee),
            }
        )

        transaction = await deployer_contract.functions.deployTokenWithLoan(
            params
        ).build_transaction(
            {
                "from": address,
                "nonce": nonce,
                "gasPrice": gas_price,
                "gas": gas_estimate,
                "value": int(loan_fee),
            }
        )

        signed_tx = chain_info.w3.eth.account.sign_transaction(
            transaction, key
        )
        tx_hash = await chain_info.w3.eth.send_raw_transaction(
            signed_tx.raw_transaction
        )

        receipt = await chain_info.w3.eth.wait_for_transaction_receipt(
            tx_hash, timeout=30
        )
        if receipt.status == 1:
            create_log = (
                deployer_contract.events.TokenDeployed().process_receipt(
                    receipt
                )
            )
            pair_log = factory_contract.events.PairCreated().process_receipt(
                receipt
            )
            return (
                create_log[0]["args"]["tokenAddress"],
                pair_log[0]["args"]["pair"],
                create_log[0]["args"]["loanID"],
            )
        else:
            return "Error deploying token"

    except Exception as e:
        return f"Error deploying token: {str(e)}"


async def deploy_token(
    chain,
    name,
    symbol,
    supply,
    percent,
    buy_tax,
    sell_tax,
    owner,
    address,
    key,
    contribution,
):
    chain_info = await chains.get_chain_info(chain)
    deployer_address = addresses.deployer_uniswap(chain)
    factory_address = addresses.factory_uniswap(chain)

    deployer_abi = abis.read("deployer")
    factory_abi = abis.read("factory")

    deployer_contract = chain_info.w3.eth.contract(
        address=chain_info.w3.to_checksum_address(deployer_address),
        abi=deployer_abi,
    )
    factory_contract = chain_info.w3.eth.contract(
        address=chain_info.w3.to_checksum_address(factory_address),
        abi=factory_abi,
    )

    deadline = tools.timestamp_deadline()
    gas_price = await chain_info.w3.eth.gas_price
    nonce = await chain_info.w3.eth.get_transaction_count(address)

    params = {
        "name": name,
        "symbol": symbol,
        "supply": int(supply),
        "teamTokens": int(percent),
        "newOwner": owner,
        "slippageTolerance": 1,
        "buyTax": int(buy_tax),
        "sellTax": int(sell_tax),
        "taxWallet": owner,
        "deadline": deadline,
    }

    try:
        gas_estimate = await deployer_contract.functions.deployToken(
            params
        ).estimate_gas(
            {
                "from": address,
                "nonce": nonce,
                "gasPrice": gas_price,
                "value": int(contribution),
            }
        )

        transaction = await deployer_contract.functions.deployToken(
            params
        ).build_transaction(
            {
                "from": address,
                "nonce": nonce,
                "gasPrice": gas_price,
                "gas": gas_estimate,
                "value": int(contribution),
            }
        )

        signed_txn = chain_info.w3.eth.account.sign_transaction(
            transaction, key
        )
        tx_hash = await chain_info.w3.eth.send_raw_transaction(
            signed_txn.raw_transaction
        )

        receipt = await chain_info.w3.eth.wait_for_transaction_receipt(
            tx_hash, timeout=30
        )
        if receipt == 1:
            create_log = (
                deployer_contract.events.TokenDeployed().process_receipt(
                    receipt
                )
            )
            pair_log = factory_contract.events.PairCreated().process_receipt(
                receipt
            )
            return create_log[0]["args"]["tokenAddress"], pair_log[0]["args"][
                "pair"
            ]
        else:
            return "Error deploying token"

    except Exception as e:
        return f"Error deploying token: {str(e)}"


async def cancel_tx(chain, address, key, gas_multiplier=1.5):
    try:
        chain_info = await chains.get_chain_info(chain)
        latest_nonce = chain_info.w3.eth.get_transaction_count(
            address, "latest"
        )
        pending_nonce = chain_info.w3.eth.get_transaction_count(
            address, "pending"
        )
        if pending_nonce == latest_nonce:
            return "No pending transactions found. No action needed."

        gas_price = await chain_info.w3.eth.gas_price
        adjusted_gas_price = int(gas_price * gas_multiplier)

        transaction = {
            "from": address,
            "to": address,
            "value": 0,
            "gas": 21000,
            "gasPrice": adjusted_gas_price,
            "nonce": pending_nonce,
            "chainId": int(chain_info.id),
        }

        signed_txn = chain_info.w3.eth.account.sign_transaction(
            transaction, key
        )
        tx_hash = await chain_info.w3.eth.send_raw_transaction(
            signed_txn.raw_transaction
        )

        receipt = await chain_info.w3.eth.wait_for_transaction_receipt(
            tx_hash, timeout=30
        )
        if receipt.status == 1:
            return f"Stuck transaction successfully replaced\n\n{chain_info.scan_tx}0x{tx_hash.hex()}"
        else:
            return "Error: Transaction failed to replace stuck transaction"

    except Exception as e:
        return f"Error sending transaction: {str(e)}"


async def estimate_gas_without_loan(
    chain, name, symbol, supply, percent, buy_tax, sell_tax, owner, loan_fee
):
    try:
        chain_info = await chains.get_chain_info(chain)
        deployer_address = addresses.deployer(chain)
        deployer_abi = abis.read("deployer")

        deployer_contract = chain_info.w3.eth.contract(
            address=chain_info.w3.to_checksum_address(deployer_address),
            abi=deployer_abi,
        )
        deadline = tools.timestamp_deadline()
        gas_price = await chain_info.w3.eth.gas_price
        nonce = await chain_info.w3.eth.get_transaction_count(addresses.DEAD)

        params = {
            "name": name,
            "symbol": symbol,
            "supply": int(supply),
            "teamTokens": int(percent),
            "newOwner": owner,
            "slippageTolerance": 1,
            "deadline": deadline,
            "description": "none",
            "twitterLink": "none",
            "telegramLink": "none",
            "websiteLink": "none",
            "tokenURI": "",
            "buyTax": int(buy_tax),
            "sellTax": int(sell_tax),
            "taxWallet": owner,
        }

        gas_estimate = (
            await deployer_contract.functions.deployTokenWithoutLoan(
                params
            ).estimate_gas(
                {
                    "from": addresses.DEAD,
                    "nonce": nonce,
                    "gasPrice": gas_price,
                    "value": int(loan_fee),
                }
            )
        )

        gas_cost = gas_estimate * gas_price
        return gas_cost
    except Exception as e:
        return f"Error estimating gas: {str(e)}"


async def estimate_gas_with_loan(
    chain,
    name,
    symbol,
    supply,
    percent,
    buy_tax,
    sell_tax,
    loan_amount,
    duration,
    owner,
    loan_fee,
):
    try:
        chain_info = await chains.get_chain_info(chain)
        deployer_address = addresses.deployer(chain)
        deployer_abi = abis.read("deployer")

        deployer_contract = chain_info.w3.eth.contract(
            address=chain_info.w3.to_checksum_address(deployer_address),
            abi=deployer_abi,
        )
        deadline = tools.timestamp_deadline()
        gas_price = await chain_info.w3.eth.gas_price
        nonce = await chain_info.w3.eth.get_transaction_count(addresses.DEAD)
        loan_contract = settings.live_loan(chain, "address")

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
            "deadline": deadline,
            "description": "none",
            "twitterLink": "none",
            "telegramLink": "none",
            "websiteLink": "none",
            "tokenURI": "",
            "buyTax": int(buy_tax),
            "sellTax": int(sell_tax),
            "taxWallet": owner,
        }

        gas_estimate = await deployer_contract.functions.deployTokenWithLoan(
            params
        ).estimate_gas(
            {
                "from": addresses.DEAD,
                "nonce": nonce,
                "gasPrice": gas_price,
                "value": int(loan_fee),
            }
        )

        gas_cost = gas_estimate * gas_price
        return gas_cost

    except Exception as e:
        return f"Error estimating gas: {str(e)}"


async def estimate_gas_uniswap(
    chain,
    name,
    symbol,
    supply,
    percent,
    buy_tax,
    sell_tax,
    owner,
    contribution,
):
    try:
        chain_info = await chains.get_chain_info(chain)
        deployer_address = addresses.deployer_uniswap(chain)
        deployer_abi = abis.read("deployer")

        deployer_contract = chain_info.w3.eth.contract(
            address=chain_info.w3.to_checksum_address(deployer_address),
            abi=deployer_abi,
        )
        deadline = tools.timestamp_deadline()
        gas_price = await chain_info.w3.eth.gas_price
        nonce = await chain_info.w3.eth.get_transaction_count(addresses.DEAD)

        params = {
            "name": name,
            "symbol": symbol,
            "supply": int(supply),
            "teamTokens": int(percent),
            "newOwner": owner,
            "slippageTolerance": 1,
            "buyTax": int(buy_tax),
            "sellTax": int(sell_tax),
            "taxWallet": owner,
            "deadline": deadline,
        }

        gas_estimate = await deployer_contract.functions.deployToken(
            params
        ).estimate_gas(
            {
                "from": addresses.DEAD,
                "nonce": nonce,
                "gasPrice": gas_price,
                "value": int(contribution),
            }
        )

        gas_cost = gas_estimate * gas_price
        return gas_cost
    except Exception as e:
        return f"Error estimating gas: {str(e)}"


async def get_pool_funds(chain):
    chain_info = await chains.get_chain_info(chain)
    contract_abi = abis.read("lendingpool")

    contract = chain_info.w3.eth.contract(
        address=chain_info.w3.to_checksum_address(
            addresses.lending_pool(chain)
        ),
        abi=contract_abi,
    )

    try:
        function_name = "availableCapital"
        function_call = getattr(contract.functions, function_name)
        result = await function_call().call()

        return chain_info.w3.from_wei(result, "ether")

    except Exception as e:
        return f"Error reading contract: {e}"


async def transfer_balance(chain, address, owner, key):
    chain_info = await chains.get_chain_info(chain)

    try:
        checksum_address = chain_info.w3.to_checksum_address(address)
        checksum_owner = chain_info.w3.to_checksum_address(owner)
        balance_wei = await chain_info.w3.eth.get_balance(checksum_address)
        gas_price = await chain_info.w3.eth.gas_price
        nonce = await chain_info.w3.eth.get_transaction_count(checksum_address)
        sample_transaction = {
            "from": checksum_address,
            "to": checksum_owner,
            "value": 1,
            "gasPrice": gas_price,
        }
        gas_estimate = await chain_info.w3.eth.estimate_gas(sample_transaction)
        gas_cost = gas_price * gas_estimate

        if balance_wei <= gas_cost:
            return "Error: Insufficient balance to cover gas costs."

        amount_to_transfer = balance_wei - gas_cost

        if chain_info.w3.from_wei(amount_to_transfer, "ether") <= 0.0001:
            return "Error: Insufficient funds to send a valid transaction."

        transaction = {
            "from": checksum_address,
            "to": checksum_owner,
            "value": amount_to_transfer,
            "gas": gas_estimate,
            "gasPrice": gas_price,
            "nonce": nonce,
            "chainId": int(chain_info.id),
        }
        signed_tx = chain_info.w3.eth.account.sign_transaction(
            transaction, key
        )
        tx_hash = await chain_info.w3.eth.send_raw_transaction(
            signed_tx.raw_transaction
        )

        receipt = await chain_info.w3.eth.wait_for_transaction_receipt(
            tx_hash, timeout=30
        )
        if receipt == 1:
            return f"0x{tx_hash.hex()}"
        else:
            return "Error transferring balance"

    except Exception as e:
        return f"Error transferring balance: {str(e)}"
