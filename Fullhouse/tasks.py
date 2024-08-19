from celery import shared_task
from market.models import MarketInfo
from datetime import datetime

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

'''
@shared_task
def update_market_info():
    # Similar logic as in the management command
    market_info, created = MarketInfo.objects.get_or_create(pk=1)
    market_info.price = 123.45
    market_info.amount_transactions += 10
    market_info.amount_players_online = 5
    market_info.amount_players_total += 1
    market_info.total_coins += 1000.00
    market_info.total_money += 500.00
    market_info.total_profit += 100.00
    market_info.updated_at = datetime.now()
    market_info.save()'''


# views.py or tasks.py
'''
def send_transaction_update():
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'transactions',
        {
            'type': 'send_transaction_update',
            'transactions': 'Updated transaction data here'
        }
    )'''