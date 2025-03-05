import aiohttp
import os

from constants.protocol import chains


class Etherscan:
    def __init__(self):
        self.url = "https://api.etherscan.io/v2/api"
        self.key = os.getenv("ETHERSCAN_API_KEY")

    async def get_native_price(self, chain):
        chain_info = await chains.get_chain_info(chain)
        if chain == "poly":
            field = "maticusd"
        else:
            field = "ethusd"

        url = f"{self.url}?chainid={chain_info.id}&module=stats&action={chain_info.native}price&apikey={self.key}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                return float(data["result"][field]) / 1**18
