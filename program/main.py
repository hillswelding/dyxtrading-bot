
from func_connections import connect_dydx, connect_public_dydx
from func_private import abort_all_positions
from func_public import construct_market_prices
from func_cointegration import store_cointegration_results
from func_entry_pairs import open_positions
from func_exit_pairs import manage_trade_exits
from func_messaging import send_message
import time
import json

from constants import (
 ABORT_ALL_POSITIONS, 
 FIND_COINTEGRATED, 
 PLACE_TRADES, 
 MANAGE_EXITS,
 RUN_BOT
)


  
# MAIN FUNCTION
if __name__ == "__main__":
  
  # Message on start
  # send_message("Bot launch successful")
  print("Bot launch successful")
  # Connect to client
  try:
    print("Connecting to Client...")
    client = connect_dydx()   
    # print("Connecting to Mainnet...")
    # public_client = connect_public_dydx()
    # print(dir(public_client))
    # exit(1)
  except Exception as e:
    print("Error connecting to client: ", e)
    send_message(f"Failed to connect to client {e}")
    exit(1)
    
 
  # Abort all open positions
  if ABORT_ALL_POSITIONS:
    try:
      print("Closing all positions...")
      close_orders = abort_all_positions(client)
    except Exception as e:
      print("Error closing all positions: ", e)
      send_message(f"Error closing all positions {e}")
      exit(1)

  # Find Cointegrated Pairs
  if FIND_COINTEGRATED:

    # Construct Market Prices
    try:
      print("Fetching market prices, please allow 3 mins...")
      df_market_prices = construct_market_prices(client, client) # change to public_client for mainnet
    except Exception as e:
      print("Error constructing market prices: ", e)
      send_message(f"Error constructing market prices {e}")
      exit(1)

    # Store Cointegrated Pairs
    try:
      print("Storing cointegrated pairs...")
      stores_result = store_cointegration_results(df_market_prices)
      if stores_result != "saved":
        print("Error saving cointegrated pairs")
        exit(1)
    except Exception as e:
      print("Error saving cointegrated pairs: ", e)
      send_message(f"Error saving cointegrated pairs {e}")
      exit(1)
      
 
  # Run as always on
  while RUN_BOT:

    # Place trades for opening positions
    if MANAGE_EXITS:
      try:
        print("Main Loop - Managing exits...")
        manage_trade_exits(client)
      except Exception as e:
        print("Main Loop - Error managing exiting positions: ", e)
        # send_message(f"Error managing exiting positions {e}")
        exit(1)

    # Place trades for opening positions
    if PLACE_TRADES:
      try:
        print("Main Loop - Finding trading opportunities...")
        open_positions(client)
      except Exception as e:
        print("Main Loop - Error trading pairs: ", e)
        # send_message(f"Error opening trades {e}")
        exit(1)
        
    time.sleep(1)
                
 