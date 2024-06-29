# API

import requests, time
from datetime import datetime
from constants import chains


class ChainScan:
    def __init__(self):
        pass
        
    def get_abi(self, contract: str, chain: str) -> str:
        if chain not in chains.chains:
            raise ValueError(f"Invalid chain: {chain}")
        chain_info = chains.chains[chain]
        url = f"{chain_info.api}?module=contract&action=getsourcecode&address={contract}{chain_info.key}"
        response = requests.get(url)
        data = response.json()
        return data["result"][0]["ABI"]


    def get_block(self, chain: str, time: "int") -> str:
        if chain not in chains.chains:
            raise ValueError(f"Invalid chain: {chain}")
        chain_info = chains.chains[chain]
        url = f"{chain_info.api}?module=block&action=getblocknobytime&timestamp={time}&closest=before{chain_info.key}"
        response = requests.get(url)
        data = response.json()
        return data["result"]


    def get_daily_tx_count(self, contract: str, chain: str, ) -> int:
        if chain not in chains.chains:
            raise ValueError(f"Invalid chain: {chain}")
        chain_info = chains.chains[chain]
        yesterday = int(time.time()) - 86400
        block_yesterday = self.get_block(chain, yesterday)
        block_now = self.get_block(chain, int(time.time()))
        tx_url = f"{chain_info.api}?module=account&action=txlist&address={contract}&startblock={block_yesterday}&endblock={block_now}&page=1&offset=1000&sort=asc{chain_info.key}"
        tx_response = requests.get(tx_url)
        tx_data = tx_response.json()
        if tx_data:
            tx_entry_count = len(tx_data['result']) if 'result' in tx_data else 0
        else:
            tx_data = 0
        internal_tx_url = f"{chain_info.api}?module=account&action=txlist&address={contract}&startblock={block_yesterday}&endblock={block_now}&page=1&offset=1000&sort=asc{chain_info.key}"
        internal_tx_response = requests.get(internal_tx_url)
        internal_tx_data = internal_tx_response.json()
        if internal_tx_data:
            internal_tx_entry_count = len(internal_tx_data['result']) if 'result' in internal_tx_data else 0
        else:
            internal_tx_data = 0
        entry_count = tx_entry_count + internal_tx_entry_count
        return entry_count


    def get_gas(self, chain):
        if chain not in chains.chains:
            raise ValueError(f"Invalid chain: {chain}")
        chain_info = chains.chains[chain]
        url = f"{chain_info.api}?module=gastracker&action=gasoracle{chain_info.key}"
        response = requests.get(url)
        return response.json()


    def get_native_balance(self, wallet, chain):
        if chain not in chains.chains:
            raise ValueError(f"Invalid chain: {chain}")
        chain_info = chains.chains[chain]
        url = f"{chain_info.api}?module=account&action=balancemulti&address={wallet}&tag=latest{chain_info.key}"
        response = requests.get(url)
        data = response.json()
        amount_raw = float(data["result"][0]["balance"])
        return f"{amount_raw / 10 ** 18}"


    def get_native_price(self, chain):
        if chain not in chains.chains:
            raise ValueError(f"Invalid chain: {chain}")
        chain_info = chains.chains[chain]

        if chain == "poly":
            field = "maticusd"
        else:
            field = "ethusd"
        
        url = f"{chain_info.api}?module=stats&action={chain_info.token}price{chain_info.key}"
        response = requests.get(url)
        data = response.json()

        return float(data["result"][field]) / 1**18


    def get_pool_liq_balance(self, wallet, token, chain):
        if chain not in chains.chains:
            raise ValueError(f"Invalid chain: {chain}")
        chain_info = chains.chains[chain]
        url = f"{chain_info.api}?module=account&action=tokenbalance&contractaddress={token}&address={wallet}&tag=latest{chain_info.key}"
        response = requests.Session().get(url)
        data = response.json()
        return int(data["result"] or 0)


    def get_stables_balance(self, wallet, token, chain):
        try:
            if chain not in chains.chains:
                raise ValueError(f"Invalid chain: {chain}")

            chain_info = chains.chains[chain]
            url = f"{chain_info.api}?module=account&action=tokenbalance&contractaddress={token}&address={wallet}&tag=latest{chain_info.key}"
            response = requests.get(url)
            data = response.json()
            return int(data["result"][:-6])
        except Exception as e:
            return 0


    def get_supply(self, token, chain):
        if chain not in chains.chains:
            raise ValueError(f"Invalid chain: {chain}")
        chain_info = chains.chains[chain]
        url = f"{chain_info.api}?module=stats&action=tokensupply&contractaddress={token}{chain_info.key}"
        response = requests.get(url)
        data = response.json()
        return data["result"]


    def get_token_balance(self, wallet, token, chain):
        try:
            if chain not in chains.chains:
                raise ValueError(f"Invalid chain: {chain}")
            chain_info = chains.chains[chain]
            url = f"{chain_info.api}?module=account&action=tokenbalance&contractaddress={token}&address={wallet}&tag=latest{chain_info.key}"
            response = requests.get(url)
            data = response.json()
            return int(data["result"][:-18])
        except Exception:
            return 0


    def get_tx_from_hash(self, tx, chain):
        if chain not in chains.chains:
            raise ValueError(f"Invalid chain: {chain}")
        chain_info = chains.chains[chain]
        url = f"{chain_info.api}?module=proxy&action=eth_getTransactionByHash&txhash={tx}{chain_info.key}"
        response = requests.get(url)
        return response.json()


    def get_tx(self, address, chain):
        if chain not in chains.chains:
            raise ValueError(f"Invalid chain: {chain}")
        chain_info = chains.chains[chain]
        url = f"{chain_info.api}?module=account&action=txlist&sort=desc&address={address}{chain_info.key}"
        response = requests.get(url)
        return response.json()


    def get_internal_tx(self, address, chain):
        if chain not in chains.chains:
            raise ValueError(f"Invalid chain: {chain}")
        chain_info = chains.chains[chain]
        url = f"{chain_info.api}?module=account&action=txlistinternal&sort=desc&address={address}{chain_info.key}"
        response = requests.get(url)
        return response.json()


    def get_liquidity_hub_data(self, hub_address, chain):
        now = datetime.now()
        if chain in chains.chains:
            chain_native = chains.chains[chain].token
        hub = self.get_internal_tx(hub_address, chain)
        hub_filter = [d for d in hub["result"] if d["from"] in f"{hub_address}".lower()]
        value_raw = int(hub_filter[0]["value"]) / 10**18
        value = round(value_raw, 3) 
        dollar = float(value) * float(self.get_native_price(chain_native))
        time = datetime.fromtimestamp(int(hub_filter[0]["timeStamp"]))
        duration = now - time
        days = duration.days
        hours, remainder = divmod(duration.seconds, 3600)
        minutes = (remainder % 3600) // 60
        return value, dollar, time, days, hours, minutes


    def get_verified(self, contract, chain):
        if chain not in chains.chains:
            raise ValueError(f"Invalid chain: {chain}")
        chain_info = chains.chains[chain]
        url = f"{chain_info.api}?module=contract&action=getsourcecode&address={contract}{chain_info.key}"
        response = requests.get(url)
        data = response.json()
        return True if "SourceCode" in data["result"][0] else False
