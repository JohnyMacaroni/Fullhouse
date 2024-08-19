import time
import requests
from django.core.management.base import BaseCommand
from market.models import Profile, Transaction, MarketInfo, UserWallet, ChatMessage

class Command(BaseCommand):
    help = 'Fetch BTC to USD conversion rate every 60 seconds'

    def handle(self, *args, **kwargs):
        while True:
            try:
                response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
                data = response.json()
                btc_to_usd = data['bitcoin']['usd']
                self.stdout.write(self.style.SUCCESS(f"BTC to USD: {btc_to_usd}"))
                market = MarketInfo.objects.get(id=1)
                market.btc_price = btc_to_usd
                market.save()
                print(market.btc_price )

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error fetching BTC to USD: {e}"))

            time.sleep(60)