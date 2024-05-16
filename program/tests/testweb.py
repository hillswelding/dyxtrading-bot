# main.py
from web3 import Web3

# Setup
alchemy_url = "https://eth-sepolia.g.alchemy.com/v2/IVBi_rOLgQ7PRgiquRQn5Ywv1DaP0VQY"
w3 = Web3(Web3.HTTPProvider(alchemy_url))

# Print if web3 is successfully connected
print("CONNECTION")
print(w3.is_connected())
print()
# Get the latest block number
latest_block = w3.eth.block_number
print("LASTEST BLOCK ", latest_block)
print()

# Get the balance of an account
balance = w3.eth.get_balance('0xcF9E5516240ff6C017E3a306e8bAC9897776EBF5')

print()
print("BALANCE")
print(balance)

# Get the information of a transaction
tx = w3.eth.get_transaction('0x79dfbc93ede228addb98ba78a7c6cf85bcb73cd0c27a72e9c957e7516d50a67f')
print()
print("TRX")
print(tx)
