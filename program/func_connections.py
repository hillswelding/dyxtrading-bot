# from decouple import config
from dydx3 import Client
from dydx3.constants import NETWORK_ID_SEPOLIA, API_HOST_MAINNET,NETWORK_ID_MAINNET
from web3 import Web3
from constants import (
  HOST,
  ETHEREUM_ADDRESS,
  ETH_PRIVATE_KEY,
  DYDX_API_KEY,
  DYDX_API_SECRET,
  DYDX_API_PASSPHRASE,
  STARK_PRIVATE_KEY,
  HTTP_PROVIDER,
  HTTP_PROVIDER_MAINNET
)

# Connect to DYDX
def connect_public_dydx():

  # Create Client Connection
  client = Client(
    network_id=NETWORK_ID_MAINNET,
    host=API_HOST_MAINNET,
    api_key_credentials={
          "key": DYDX_API_KEY,
          "secret": DYDX_API_SECRET,
          "passphrase": DYDX_API_PASSPHRASE,
      },
    stark_private_key=STARK_PRIVATE_KEY,
    eth_private_key=ETH_PRIVATE_KEY,
    default_ethereum_address=ETHEREUM_ADDRESS,
    web3=Web3(Web3.HTTPProvider(HTTP_PROVIDER_MAINNET)),
  )
  # Return Client
  return client


# Connect to DYDX
def connect_dydx():

  # Create Client Connection
  client = Client(
      network_id=NETWORK_ID_SEPOLIA,
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

  # Confirm client
  account = client.private.get_account()
  account_id = account.data["account"]["id"]
  quote_balance = account.data["account"]["quoteBalance"]
  print("Connection Successful")
  print("Account ID: ", account_id)
  print("Quote Balance: ", quote_balance)

  # Return Client
  return client
