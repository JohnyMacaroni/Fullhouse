from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_user = models.IntegerField(default=0)
    coins = models.IntegerField(default=0)
    money = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    btc = models.DecimalField(max_digits=10, decimal_places=7, default=0.00)
    
    def __str__(self):
        return self.user.username


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction by {self.user.username} for {self.amount} at {self.price}"
    

class MarketInfo(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    amount_transactions = models.PositiveIntegerField(default=0)
    amount_players_online = models.PositiveIntegerField(default=0)
    amount_players_total = models.PositiveIntegerField(default=0)
    total_coins = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total_money = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total_profit = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    btc_price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Market Info as of {self.updated_at}"
    

class UserWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wallet_address = models.CharField(max_length=255)
    private_key = models.CharField(max_length=512)
    name = models.CharField(max_length=512,default=wallet_address)

    def __str__(self):
        return f"{self.user.username}'s Wallet"
    

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)