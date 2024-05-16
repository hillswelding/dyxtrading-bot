import time
from dydx3 import Client
from dydx3.constants import API_HOST_SEPOLIA 
from dydx3.constants import MARKET_BTC_USD
from dydx3.constants import NETWORK_ID_SEPOLIA
from dydx3.constants import ORDER_SIDE_BUY
from dydx3.constants import ORDER_STATUS_OPEN
from dydx3.constants import ORDER_TYPE_LIMIT
from dydx3.constants import ORDER_TYPE_MARKET
from web3 import Web3
from datetime import datetime, timedelta
import time

ETHEREUM_ADDRESS = "0xcF9E5516240ff6C017E3a306e8bAC9897776EBF5"
ETH_PRIVATE_KEY = "0x49e81dbae6a94003aa16781fdc745570d33403ea711055d25a65fad481b6eb50"

STARK_PRIVATE_KEY = "07cdb5e987958ff1c1c2f9e0c9fd04ce3c6c301a0e791f9920621a9a64bf9f17"
DYDX_API_KEY = "16359144-f584-3efa-1e47-c5f8f7ba32bd"
DYDX_API_SECRET = "m7-8sYHY9QBcVAcsFLrmQdER2te9t3JMlcMXKCln"
DYDX_API_PASSPHRASE = "HwroxxRrP1OkDbZWztoZ"
HOST = API_HOST_SEPOLIA#"https://api.stage.dydx.exchange"

print(API_HOST_SEPOLIA)
# HTTP Provider
HTTP_PROVIDER = "https://eth-sepolia.g.alchemy.com/v2/IVBi_rOLgQ7PRgiquRQn5Ywv1DaP0VQY"

# https://github.com/dydxprotocol/dydx-v3-python/blob/master/examples/orders.py

client = Client(
    network_id=NETWORK_ID_SEPOLIA,
    host=API_HOST_SEPOLIA,
        api_key_credentials={
        "key": DYDX_API_KEY,
        "secret": DYDX_API_SECRET,
        "passphrase": DYDX_API_PASSPHRASE,
    },
    stark_private_key=STARK_PRIVATE_KEY,
    eth_private_key=ETH_PRIVATE_KEY,
    default_ethereum_address=ETHEREUM_ADDRESS,
    web3=Web3(Web3.HTTPProvider(HTTP_PROVIDER)),
)
stark_key_pair_with_y_coordinate = client.onboarding.derive_stark_key()
client.stark_private_key = stark_key_pair_with_y_coordinate['private_key']
(public_x, public_y) = (
    stark_key_pair_with_y_coordinate['public_key'],
    stark_key_pair_with_y_coordinate['public_key_y_coordinate']
)

print(stark_key_pair_with_y_coordinate)
print(client.stark_private_key)
print()
print(dir(client))

account = client.private.get_account()
account_id = account.data["account"]["id"]
quote_balance = account.data["account"]["quoteBalance"]
# print(account.data)
print("Connection successful")
print("Account Id: ", account_id)
print("Quote Balance: ", quote_balance)
print()

# OHLC Candlestick Data
candles = client.public.get_candles(
    market="BTC-USD",
    resolution='1HOUR',
    limit=3
)

# PPrint Result
# pprint(candles.data["candles"][0])
print(candles.data["candles"][0]['close'])
print()
# Cancel all orders.
client.private.cancel_all_orders()
time.sleep(5)
  
# Get Position Id
account_response = client.private.get_account()
position_id = account_response.data["account"]["positionId"]
print()
print(position_id)
print()

order_params = {
    'position_id': position_id,
    'market': MARKET_BTC_USD,
    'side': ORDER_SIDE_BUY,
    'order_type': ORDER_TYPE_MARKET,
    'post_only': False,
    'size': '0.001',
    'price': '100000',
    'limit_fee': '0.0015',
    'expiration_epoch_seconds': time.time() + 70,
    'time_in_force':'FOK',
    'reduce_only':False
}
order_response = client.private.create_order(**order_params)
order_id = order_response.data['order']['id']
print()
print(order_id)
print()
print(order_response.data)

