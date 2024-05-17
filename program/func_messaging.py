import requests
from decouple import config
from constants import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

# Send Message
def send_message(message):
  
  bot_token = config(TELEGRAM_TOKEN, default=TELEGRAM_TOKEN)
  chat_id = config(TELEGRAM_CHAT_ID, default=TELEGRAM_CHAT_ID)
  url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}"
  try:
    res = requests.get(url)    
    if res.status_code == 200:
      return f"success - {res.status_code}"  
    else:
      return f"failed - {res.status_code}"  
  except Exception as e:
          print(f"Couldn't Send Message - {e}")
