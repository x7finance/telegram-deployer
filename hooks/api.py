import os, requests

from constants import chains


class ChainScan:
    def __init__(self):
        self.url = "https://api.etherscan.io/v2/api"
        self.key = os.getenv('ETHERSCAN_API_KEY')
        
    def get_abi(self, contract: str, chain: str) -> str:
        chain_info = chains.chains[chain]
        url = f"{self.url}?chainid={chain_info.id}&module=contract&action=getsourcecode&address={contract}&apikey={self.key}"
        response = requests.get(url)
        data = response.json()
        return data["result"][0]["ABI"]


    def get_block(self, time: "int", chain: str) -> str:
        chain_info = chains.chains[chain]
        url = f"{self.url}?chainid={chain_info.id}&module=block&action=getblocknobytime&timestamp={time}&closest=before&apikey={self.key}"
        response = requests.get(url)
        data = response.json()
        return data["result"]


    def get_gas(self, chain: str):
        chain_info = chains.chains[chain]
        url = f"{self.url}?chainid={chain_info.id}&module=gastracker&action=gasoracle&apikey={self.key}"
        response = requests.get(url)
        return response.json()


    def get_native_balance(self, wallet, chain):
        chain_info = chains.chains[chain]
        url = f"{self.url}?chainid={chain_info.id}&module=account&action=balancemulti&address={wallet}&tag=latest&apikey={self.key}"
        response = requests.get(url)
        data = response.json()
        amount_raw = float(data["result"][0]["balance"])
        return f"{amount_raw / 10 ** 18}"


    def get_native_price(self, chain):
        chain_info = chains.chains[chain]
        if chain == "poly":
            field = "maticusd"
        else:
            field = "ethusd"
        
        url = f"{self.url}?chainid={chain_info.id}&module=stats&action={chain_info.native}price&apikey={self.key}"
        response = requests.get(url)
        data = response.json()

        return float(data["result"]["ethusd"]) / 1**18