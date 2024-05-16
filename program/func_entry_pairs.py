from constants import ZSCORE_THRESH, USD_PER_TRADE, USD_MIN_COLLATERAL
from func_utils import format_number
from func_public import get_candles_recent
from func_cointegration import calculate_zscore
from func_private import is_open_positions
from func_bot_agent import BotAgent
import pandas as pd
import json

from pprint import pprint


# Open positions
def open_positions(client):

  """
    Manage finding triggers for trade entry
    Store trades for managing later on on exit function
  """

  # Load cointegrated pairs
  df = pd.read_csv("cointegrated_pairs.csv")

  # Get markets from referencing of min order size, tick size etc
  markets = client.public.get_markets().data

  # Initialize container for BotAgent results
  bot_agents = []

  # Opening JSON file
  try:
    open_positions_file = open("bot_agents.json")
    open_positions_dict = json.load(open_positions_file)
    for p in open_positions_dict:
      bot_agents.append(p)
      # pprint(bot_agents)
  except:
    bot_agents = []
  
  # Find ZScore triggers
  for index, row in df.iterrows():    
    
    # Extract variables
    base_market = row["base_market"]
    quote_market = row["quote_market"]
    hedge_ratio = row["hedge_ratio"]
    half_life = row["half_life"]
    # print(f"In open_positions: {base_market} - {quote_market}")
    
    # Get prices
    series_1 = get_candles_recent(client, base_market)
    series_2 = get_candles_recent(client, quote_market)
    try:
      # Get ZScore
      if len(series_1) > 0 and len(series_1) == len(series_2):
        spread = series_1 - (hedge_ratio * series_2)
        z_score = calculate_zscore(spread).values.tolist()[-1] # Get latest Z Score
        # print("-----")
        # print(f"Z Score: {z_score} Postive Z Treshold {ZSCORE_THRESH} - Negitive Z Threshold: {-ZSCORE_THRESH}")
        # print("-----")
        # Establish if potential trade
        if abs(z_score) >= ZSCORE_THRESH:
        # if -ZSCORE_THRESH < z_score < ZSCORE_THRESH:
       
          # print("-----")
          # print(f"Z Score: {z_score} Suitable for Trade Position")
          # print("The absolute value of z_score is within the range [-1.5, 1.5).")
          # print("-----")
          # Ensure like-for-like not already open (diversify trading)
          is_base_open = is_open_positions(client, base_market)
          is_quote_open = is_open_positions(client, quote_market)

          # Place trade
          if not is_base_open and not is_quote_open:

            # Determine side
            base_side = "BUY" if z_score < 0 else "SELL"
            quote_side = "BUY" if z_score > 0 else "SELL"

            # Get acceptable price in string format with correct number of decimals
            base_price = series_1[-1]
            quote_price = series_2[-1]
            # Better Price would be a Quote from DYDX rather thans the Close
            # BASE PRICE
            # if the Z Score is less than 0 then base_price BUY 1% higher than the ASK Price
            # if Z Score is greater than 0 then base_price SELL 1% lower than BUY Price
            accept_base_price = float(base_price) * 1.01 if z_score < 0 else float(base_price) * 0.99
            
            # QUOTE PRICE
            # if the Z Score is less than 0 then quote_price SELL 1% lower than the BUY Price
            # if Z Score is greater than 0 then quote_price BUY 1% higher than ASK Price
            accept_quote_price = float(quote_price) * 1.01 if z_score > 0 else float(quote_price) * 0.99
            # If we close a trade this guarentees a CLOSE Trade
            failsafe_base_price = float(base_price) * 0.05 if z_score < 0 else float(base_price) * 1.7
            
            
            base_tick_size = markets["markets"][base_market]["tickSize"]
            quote_tick_size = markets["markets"][quote_market]["tickSize"]

            # Format prices
            accept_base_price = format_number(accept_base_price, base_tick_size)
            accept_quote_price = format_number(accept_quote_price, quote_tick_size)
            accept_failsafe_base_price = format_number(failsafe_base_price, base_tick_size)
           
            # Get size
            base_quantity = 1 / base_price * USD_PER_TRADE
            quote_quantity = 1 / quote_price * USD_PER_TRADE
            base_step_size = markets["markets"][base_market]["stepSize"]
            quote_step_size = markets["markets"][quote_market]["stepSize"]

            # Format sizes
            base_size = format_number(base_quantity, base_step_size)
            quote_size = format_number(quote_quantity, quote_step_size)

            # Ensure size
            base_min_order_size = markets["markets"][base_market]["minOrderSize"]
            quote_min_order_size = markets["markets"][quote_market]["minOrderSize"]
            check_base = float(base_quantity) > float(base_min_order_size)
            check_quote = float(quote_quantity) > float(quote_min_order_size)
          
            # If checks pass, place trades
            if check_base and check_quote:
              
              # print()
              # print(f"Base Price: {accept_base_price}")
              # print(f"Quote Price: {accept_quote_price}")
              # print(f"FailSafe Price: {accept_failsafe_base_price}")
              # print()
            
              # print()
              # print(f"Base Min Order Size: {base_min_order_size} Base-Min: {check_base}")
              # print(f"Quote Min Order Size: {quote_min_order_size} Quote-Min: {check_quote}")   
              # print()

              # Check account balance
              account = client.private.get_account()
              free_collateral = float(account.data["account"]["freeCollateral"])
              # print(f"Current Account Balance: {free_collateral} Minimum amount before trading stops: {USD_MIN_COLLATERAL}")

              # Guard: Ensure collateral
              if free_collateral <= USD_MIN_COLLATERAL:
                print(f"Current Account Balance: {free_collateral} Free Collateral Exceeded : {USD_MIN_COLLATERAL}")
                break

              # Create Bot Agent
              bot_agent = BotAgent(
                client,
                market_1=base_market,
                market_2=quote_market,
                base_side=base_side,
                base_size=base_size,
                base_price=accept_base_price,
                quote_side=quote_side,
                quote_size=quote_size,
                quote_price=accept_quote_price,
                accept_failsafe_base_price=accept_failsafe_base_price,
                z_score=z_score,
                half_life=half_life,
                hedge_ratio=hedge_ratio
              )

              # Open Trades
              bot_open_dict = bot_agent.open_trades()
              # print()
              # print(f"Bot Agent Dict :{bot_open_dict}") 
              # print()
              # Guard: Handle failure
              if bot_open_dict is None or bot_open_dict == "failed":
                print()
                print(f"Bot Agent Dict is NULL") 
                print()
                continue

              # Handle success in opening trades
              if bot_open_dict["pair_status"] == "LIVE":

                # Append to list of bot agents
                bot_agents.append(bot_open_dict)
                del(bot_open_dict)

                # Confirm live status in print
                print("---")
                print("Trade status: Live")
                print("---")
    
    # This was causing an EXIT from the BOT
    except Exception as e:
     print("Exception Error:", e)
     print(f"Error in open_positions: {base_market} - {quote_market}")
     continue
     
  # Save agents
  print(f"Storing Trades (bot_agents) file -  Success: Manage open trades checked")
  if len(bot_agents) > 0:
    with open("bot_agents.json", "w") as f:
      json.dump(bot_agents, f)
