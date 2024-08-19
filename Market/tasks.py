
from .models import Profile, Transaction, MarketInfo, UserWallet, ChatMessage

import requests
import schedule
import time

def get_btc_to_usd():
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
        data = response.json()
        btc_to_usd = data['bitcoin']['usd']
        market = MarketInfo.objects.get(id=1)
        market.btc_price = btc_to_usd
        market.save()
        
    except Exception as e:
        print(f"Error fetching BTC to USD: {e}")

def start_scheduler():
    schedule.every(60).seconds.do(get_btc_to_usd)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    start_scheduler()