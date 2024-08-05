
from statistics import mode
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from pkg_resources import require
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Info(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    Money = models.IntegerField(default=0)
    Coins = models.IntegerField(default=0)
    Profit = models.IntegerField(default=0)



class transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_username = models.CharField(max_length=64,null=True,blank=True)
    Coins = models.PositiveIntegerField (default=0)
    Price = models.PositiveIntegerField (default=0)
    pp = models.PositiveIntegerField (default=0, null=True,blank=True)
    active = models.BooleanField(default= True )

'''
class Message(models.Model):
    sender = models.CharField(max_length=64)
    message=models.CharField(max_length=64)
'''
 
 
class Global_Info(models.Model):
    moneyin = models.IntegerField(default=0)
    Totalcoins = models.IntegerField(default=0)
    Totalprofit = models.IntegerField(default=0)
    Players_online = models.IntegerField(default=0) 
    currency_value = models.IntegerField(default=0)