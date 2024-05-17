from dydx3.constants import API_HOST_MAINNET
from dydx3.constants import API_HOST_SEPOLIA 
from decouple import config

# !!!! SELECT MODE !!!!
MODE = "DEVELOPMENT"

# Close all open positions and orders
ABORT_ALL_POSITIONS = True

# Find Cointegrated Pairs
FIND_COINTEGRATED = False

# Run Bot
RUN_BOT = True

# Manage Exits
MANAGE_EXITS = True

# Place Trades
PLACE_TRADES = True


# Resolution
RESOLUTION = "1HOUR" # 1DAY, 4HOURS, 1HOUR, 30MINS, 15MINS, 5MINS, 1MIN.

# Stats Window
WINDOW = 21

# Thresholds - Opening
MAX_HALF_LIFE = 24 # Spread should Cross the Zero line often so Half life should be between 0 and 24
ZSCORE_THRESH = 1.5
USD_PER_TRADE = 100
USD_MIN_COLLATERAL = 100 # 1880

# Thresholds - Closing
CLOSE_AT_ZSCORE_CROSS = True

# Ethereum Address
ETHEREUM_ADDRESS = "0xcF9E5516240ff6C017E3a306e8bAC9897776EBF5"
ETH_PRIVATE_KEY = "0x49e81dbae6a94003aa16781fdc745570d33403ea711055d25a65fad481b6eb50"

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
STARK_PRIVATE_KEY_TEXT = "07cdb5e987958ff1c1c2f9e0c9fd04ce3c6c301a0e791f9920621a9a64bf9f17"
DYDX_API_KEY_TEXT = "16359144-f584-3efa-1e47-c5f8f7ba32bd"
DYDX_API_SECRET_TEXT = "m7-8sYHY9QBcVAcsFLrmQdER2te9t3JMlcMXKCln"
DYDX_API_PASSPHRASE_TEXT = "HwroxxRrP1OkDbZWztoZ"

# KEYS - PRODUCTION
# Must be on Mainnet in DYDX
STARK_PRIVATE_KEY_MAINNET = ""#config("STARK_PRIVATE_KEY_MAINNET")
DYDX_API_KEY_MAINNET = ""#config("DYDX_API_KEY_MAINNET")
DYDX_API_SECRET_MAINNET = ""#config("DYDX_API_SECRET_MAINNET")
DYDX_API_PASSPHRASE_MAINNET = ""#config("DYDX_API_PASSPHRASE_MAINNET")

# KEYS - DEVELOPMENT
# Must be on Testnet in DYDX
STARK_PRIVATE_KEY_TESTNET = config(STARK_PRIVATE_KEY_TEXT, default=STARK_PRIVATE_KEY_TEXT)
DYDX_API_KEY_TESTNET = config(DYDX_API_KEY_TEXT, default=DYDX_API_KEY_TEXT)
DYDX_API_SECRET_TESTNET =config(DYDX_API_SECRET_TEXT, default=DYDX_API_SECRET_TEXT)
DYDX_API_PASSPHRASE_TESTNET = config(DYDX_API_PASSPHRASE_TEXT, default=DYDX_API_PASSPHRASE_TEXT)

# KEYS - Export
STARK_PRIVATE_KEY = STARK_PRIVATE_KEY_MAINNET if MODE == "PRODUCTION" else STARK_PRIVATE_KEY_TESTNET
DYDX_API_KEY = DYDX_API_KEY_MAINNET if MODE == "PRODUCTION" else DYDX_API_KEY_TESTNET
DYDX_API_SECRET = DYDX_API_SECRET_MAINNET if MODE == "PRODUCTION" else DYDX_API_SECRET_TESTNET
DYDX_API_PASSPHRASE = DYDX_API_PASSPHRASE_MAINNET if MODE == "PRODUCTION" else DYDX_API_PASSPHRASE_TESTNET

# HOST - Export
HOST = API_HOST_MAINNET if MODE == "PRODUCTION" else API_HOST_SEPOLIA

# HTTP PROVIDER
HTTP_PROVIDER_MAINNET = "https://mainnet.infura.io/v3/42ef9289b2294414972f42b0cfdfd0d3"#"https://eth-mainnet.g.alchemy.com/v2/C38A2E03uos12XB0zaw4OhkHEZm5Io8T"
HTTP_PROVIDER_TESTNET = "https://eth-sepolia.g.alchemy.com/v2/IVBi_rOLgQ7PRgiquRQn5Ywv1DaP0VQY"
HTTP_PROVIDER = HTTP_PROVIDER_MAINNET if MODE == "PRODUCTION" else HTTP_PROVIDER_TESTNET


