import requests

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
        
        url = f"{chain_info.api}?module=stats&action={chain_info.native}price{chain_info.key}"
        response = requests.get(url)
        data = response.json()

        return float(data["result"][field]) / 1**18