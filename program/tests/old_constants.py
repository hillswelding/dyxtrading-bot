# from dydx3.constants import  API_HOST_MAINNET
from decouple import config

# !!!! SELECT MODE !!!!
MODE = "DEVELOPMENT"

# Close all open positions and orders
ABORT_ALL_POSITIONS = False

# Find Cointegrated Pairs
FIND_COINTEGRATED = True

# Manage Exits
MANAGE_EXITS = True

# Place Trades
PLACE_TRADES = True

# Resolution
RESOLUTION = "1HOUR"

# Stats Window
WINDOW = 21

# Thresholds - Opening
MAX_HALF_LIFE = 24
ZSCORE_THRESH = 1.5
USD_PER_TRADE = 100
USD_MIN_COLLATERAL = 1000

# Thresholds - Closing
CLOSE_AT_ZSCORE_CROSS = True


"""
ETHEREUM_ADDRESS = "0xcF9E5516240ff6C017E3a306e8bAC9897776EBF5"
ETH_PRIVATE_KEY = "0x49e81dbae6a94003aa16781fdc745570d33403ea711055d25a65fad481b6eb50"

STARK_PRIVATE_KEY = "07cdb5e987958ff1c1c2f9e0c9fd04ce3c6c301a0e791f9920621a9a64bf9f17"
DYDX_API_KEY = "16359144-f584-3efa-1e47-c5f8f7ba32bd"
DYDX_API_SECRET = "m7-8sYHY9QBcVAcsFLrmQdER2te9t3JMlcMXKCln"
DYDX_API_PASSPHRASE = "HwroxxRrP1OkDbZWztoZ"
HOST = API_HOST_SEPOLIA
HOST = "https://api.stage.dydx.exchange"
# HTTP Provider
HTTP_PROVIDER = "https://eth-sepolia.g.alchemy.com/v2/IVBi_rOLgQ7PRgiquRQn5Ywv1DaP0VQY"
"""
ETHEREUM_ADDRESS = "0xcF9E5516240ff6C017E3a306e8bAC9897776EBF5"
ETH_PRIVATE_KEY = "0x49e81dbae6a94003aa16781fdc745570d33403ea711055d25a65fad481b6eb50"

STARK_PRIVATE_KEY = "07cdb5e987958ff1c1c2f9e0c9fd04ce3c6c301a0e791f9920621a9a64bf9f17"
DYDX_API_KEY = "16359144-f584-3efa-1e47-c5f8f7ba32bd"
DYDX_API_SECRET = "m7-8sYHY9QBcVAcsFLrmQdER2te9t3JMlcMXKCln"
DYDX_API_PASSPHRASE = "HwroxxRrP1OkDbZWztoZ"
HOST = "https://api.stage.dydx.exchange"

# HTTP Provider
HTTP_PROVIDER = "https://eth-sepolia.g.alchemy.com/v2/IVBi_rOLgQ7PRgiquRQn5Ywv1DaP0VQY"
