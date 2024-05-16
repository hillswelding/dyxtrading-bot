from dydx.client import Client
from web3 import Web3
from pprint import pprint
from datetime import datetime, timedelta
import time
# import dydx3

ETHEREUM_ADDRESS = "0xcF9E5516240ff6C017E3a306e8bAC9897776EBF5"
ETH_PRIVATE_KEY = "0x49e81dbae6a94003aa16781fdc745570d33403ea711055d25a65fad481b6eb50"

STARK_PRIVATE_KEY = "07cdb5e987958ff1c1c2f9e0c9fd04ce3c6c301a0e791f9920621a9a64bf9f17"
DYDX_API_KEY = "16359144-f584-3efa-1e47-c5f8f7ba32bd"
DYDX_API_SECRET = "m7-8sYHY9QBcVAcsFLrmQdER2te9t3JMlcMXKCln"
DYDX_API_PASSPHRASE = "HwroxxRrP1OkDbZWztoZ"
HOST = "https://api.stage.dydx.exchange"

# HTTP Provider
HTTP_PROVIDER = "https://eth-sepolia.g.alchemy.com/v2/IVBi_rOLgQ7PRgiquRQn5Ywv1DaP0VQY"

client = Client(
    host=HOST,
    api_key_credentials={
        "key": DYDX_API_KEY,
        "secret": DYDX_API_SECRET,
        "passphrase": DYDX_API_PASSPHRASE,
    },
    stark_private_key=STARK_PRIVATE_KEY,
    eth_private_key=ETH_PRIVATE_KEY,
    default_ethereum_address=ETHEREUM_ADDRESS,
    web3=Web3(Web3.HTTPProvider(HTTP_PROVIDER))
)

print(dir(client))
# print(dydx3.constants)
# Check Connection
account = client.private.get_account()
account_id = account.data["account"]["id"]
quote_balance = account.data["account"]["quoteBalance"]
# print(account.data)
print("Connection successful")
print("Account Id: ", account_id)
print("Quote Balance: ", quote_balance)

# OHLC Candlestick Data
candles = client.public.get_candles(
    market="BTC-USD",
    resolution='1HOUR',
    limit=3
)

# PPrint Result
# pprint(candles.data["candles"][0])
print(candles.data["candles"][0]['close'])


# BUY - LONG

# Get Position Id
account_response = client.private.get_account()
position_id = account_response.data["account"]["positionId"]
# print(dir(account_response))
print(position_id)
# Get expiration time
server_time = client.public.get_time()
expiration = datetime.fromisoformat(
    server_time.data["iso"].replace("Z", "")) + timedelta(seconds=70)

print(expiration)
# p = float(candles.data["candles"][0]['close'])
# p = p * 10
# print(p)

# Place an order
# placed_order = client.private.create_order(
#     position_id=position_id,  # required for creating the order signature
#     market="BTC-USD",
#     side="BUY",
#     order_type="MARKET",
#     post_only=False,
#     size='0.001',
#     price='100000',
#     limit_fee='0.015',
#     expiration_epoch_seconds=expiration.timestamp(),
#     time_in_force="FOK",
#     reduce_only=False
# )

# # PPrint order
# print(placed_order.data)
