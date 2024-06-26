from datetime import datetime, timedelta
from func_utils import format_number
import time
import json
from dydx3.constants import ORDER_TYPE_MARKET
from pprint import pprint


# Get existing open positions
def is_open_positions(client, market):

  # Protect API
  time.sleep(0.2)

  # Get positions
  all_positions = client.private.get_positions(
    market=market,
    status="OPEN"
  )
  # Protect API
  time.sleep(0.2)
  # Determine if open
  if len(all_positions.data["positions"]) > 0:
    # print()
    # print(f'CURRENT OPEN POSITIONS: {all_positions.data["positions"]}')
    # print()
    return True
  else:
    # print()
    # print("NO OPEN POSITIONS...")
    # print()
    return False


# Check order status
def check_order_status(client, order_id):
  order = client.private.get_order_by_id(order_id)
  if order.data:
    if "order" in order.data.keys():
      return order.data["order"]["status"]
  return "FAILED"


# Place market order
def place_market_order(client, market, side, size, price, reduce_only):
  # Get Position Id
  account_response = client.private.get_account()
  position_id = account_response.data["account"]["positionId"]

  order_params = {
      'position_id': position_id,
      'market': market,
      'side': side,
      'order_type': ORDER_TYPE_MARKET,
      'post_only': False,
      'size': size,
      'price': price,
      'limit_fee': '0.0015',
      'expiration_epoch_seconds': time.time() + 70,
      'time_in_force':'FOK',
      'reduce_only':reduce_only
  }
  placed_order = client.private.create_order(**order_params)
  # print(placed_order.data)

  # Return result
  return placed_order.data


# Abort all open positions
def abort_all_positions(client):
  
  # Cancel all orders
  client.private.cancel_all_orders()

  # Protect API
  time.sleep(1)

  # Get markets for reference of tick size
  markets = client.public.get_markets().data

  # Protect API
  time.sleep(1)

  # Get all open positions
  positions = client.private.get_positions(status="OPEN")
  all_positions = positions.data["positions"]

  # Handle open positions
  close_orders = []
  if len(all_positions) > 0:

    # Loop through each position
    for position in all_positions:

      # Determine Market
      market = position["market"]

      # Determine Side
      side = "BUY"
      if position["side"] == "LONG":
        side = "SELL"

      # Get Price
      price = float(position["entryPrice"])
      accept_price = price * 1.7 if side == "BUY" else price * 0.3
      tick_size = markets["markets"][market]["tickSize"]
      accept_price = format_number(accept_price, tick_size)

      # Place order to close
      order = place_market_order(
        client,
        market,
        side,
        position["sumOpen"],
        accept_price,
        True
      )

      # Append the result
      close_orders.append(order)

      # Protect API
      time.sleep(0.2)

    # Override json file with empty list
    bot_agents = []
    with open("bot_agents.json", "w") as f:
      json.dump(bot_agents, f)

    # Return closed orders
    return close_orders
