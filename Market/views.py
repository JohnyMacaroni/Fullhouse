from asyncio.windows_events import NULL
from multiprocessing import context
from urllib.request import Request
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django.core import serializers
from django.http import JsonResponse

from django. contrib. auth. decorators import login_required 
from django.views.decorators.csrf import csrf_exempt

from .forms import  TransactionForm_sell, TransactionForm_buy
from .models import  Info , transaction, Global_Info


class Global:

    Global_Info_object = Global_Info.objects.get(id=1)

    #Global_Info_object = Global_Info()
    
    moneyin = Global_Info_object.moneyin
    coins = Global_Info_object.Totalcoins
    Global_Info_object.Players_online = 0
    Players_online = 0
    
    Global_Info_object.save()

    def set_paramaters_moneyin(self, moneyin):
        self.moneyin += moneyin
        self.Global_Info_object.moneyin = self.moneyin
        
        self.Global_Info_object.save()

    def set_paramaters_Players_online(self, Player):
        self.Players_online += Player
        self.Global_Info_object.Players_online = self.Players_online

        self.Global_Info_object.save()

    def set_paramaters_coins(self, coins):
        self.coins += coins
        self.Global_Info_object.coins = self.coins

        self.Global_Info_object.save()


    def currency_value(self):
        self.Global_Info_object.value = self.coins + self.moneyin
        self.Global_Info_object.save()

        return self.Global_Info_object.value


Global_Information = Global()


def index(request):

    if request.user.is_authenticated:
        username = request.user.username

        user_object = User.objects.get(username=username)
        Info_object = Info.objects.get(user=user_object)

        #form_mesage = MessageForm(initial={'sender': username })
        form_mesage = 1
        form_transaction_sell= TransactionForm_sell(initial={'user': user_object,'user_username': username})
        form_transaction_buy= TransactionForm_buy()
    else:
        Info_object = {}
        form_mesage = ""
        form_transaction_sell = ""
        form_transaction_buy= ""

    return render(request, "market/layout.html", { "form_mesage" : form_mesage, "user_data" : Info_object, "form_transaction_sell" : form_transaction_sell,
                                                   "form_transaction_buy" : form_transaction_buy,"Global_Information": Global_Information})



def login_p(request):
    if request.method == "POST":
        # Accessing username and password from form data
        username = request.POST.get("username","")
        password = request.POST.get('password', "")
        

        # Check if username and password are correct, returning User object if so
        user = authenticate(request, username=username, password=password)
        
        # If user object is returned, log in and route to index page:
        if user: 
            login(request, user)
            Global_Information.set_paramaters_Players_online(Player=1)
            return HttpResponseRedirect(reverse("index"))
        # Otherwise, return login page again with new context
        else:
            return render(request, "market/login.html", {
                "message": "Invalid Credentials"
            })
    return render(request, "market/login.html")



def logout_p(request):
    logout(request)
    Global_Information.set_paramaters_Players_online(Player= -1)

    return HttpResponseRedirect(reverse("index"))


def register_p(request):
    if request.method == "POST":
        username = request.POST.get("username","")
        password = request.POST.get('password', "")
        email = request.POST.get("email","")

        if User.objects.filter(username=username).exists():
            return render(request, "market/register.html",{
                "status": "Username already exists!"
            })
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            user_Info=Info(user=user)
            user_Info.save()

            login(request, user)

            return HttpResponseRedirect(reverse("index"))

    return render(request, "market/register.html")


'''
@csrf_exempt
def sender(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    
    if is_ajax and request.method == "POST":
        pk_message = int(request.POST.get("pk_message"))
        message = Message.objects.filter(id__gte = pk_message+1)
        men_instance = serializers.serialize('json',  message )

        pk_transaction = int(request.POST.get("pk_transaction"))
        transactions = transaction.objects.filter(id__gte = pk_transaction+1, active = True)
        trans_instance = serializers.serialize('json',  transactions )
        
        
        return JsonResponse({"Message": men_instance , "Transactions" : trans_instance}, status=200)
        
        
    return JsonResponse({"error": ""}, status=400)
'''


@login_required
def taker(request,slug):
    
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if is_ajax and request.method == "POST":
        username = request.user.username

        if slug == "taker-transaction-sell":

            form = TransactionForm_sell(request.POST)

            if form.is_valid():
                
                user_object = User.objects.get(username=username)
                Info_object = Info.objects.get(user=user_object)
                
                Info_object.Coins -= form.cleaned_data.get('Coins')
                Info_object.pp = form.Coins/form.Price

                Info_object.save()

                form.save()
                return JsonResponse({"instance": "sucess"}, status=200)

            else:
                # some form errors occured.
                return JsonResponse({"error": form.errors}, status=400)

        elif slug == "taker-transaction-buy-house":


            form = TransactionForm_buy(request.POST)

            if form.is_valid():
                
                
                user_object = User.objects.get(username=username)
                Info_object = Info.objects.get(user=user_object)

                coins = form.cleaned_data.get('coin')

                Info_object.Money -= (coins * Global_Information.currency_value())
                Info_object.Coins += coins
                Info_object.save()
                
                return JsonResponse({"instance": "sucess"}, status=200)

            else:
                # some form errors occured.
                return JsonResponse({"error": form.errors}, status=400)

        elif slug == "taker-transaction-buy-player":

            form = TransactionForm_buy(request.POST)

            if form.is_valid():
                coins = form.cleaned_data.get('coin')
                pk = form.cleaned_data.get('pk')
                pp = form.cleaned_data.get('pp')
                print('here:')
                print(pp)
                print(pk)

                user_object = User.objects.get(username=username)
                Info_object_buyer = Info.objects.get(user=user_object)
                transaction_object = transaction.objects.get(id=int(pk))
                pp = transaction_object.pp 
                Info_object_seller = Info.objects.get(user=transaction_object.user)

                if transaction_object.active :
                    money_spent = coins*pp
                    if coins <= transaction_object.Coins and Info_object_buyer.Money >= money_spent:
                        Info_object_buyer.Money -= money_spent
                        Info_object_buyer.Coins += coins
                        Info_object_buyer.save()

                        Info_object_seller.Money += money_spent

                        transaction_object.Coins -= coins
                        
                        if transaction_object.Coins == 0: #<0.1
                            
                            transaction_object.active = False
                            
                        transaction_object.save()
                        
                        return JsonResponse({"instance": "sucess"}, status=200)

                    return JsonResponse({"error": form.errors}, status=400)
                return JsonResponse({"error": form.errors}, status=400)

            else:
                # some form errors occured.
                return JsonResponse({"error": form.errors}, status=400)

        elif  slug == "taker-mesage":

            #form = MessageForm(request.POST)

            if form.is_valid():
                form.save()
                return JsonResponse({"instance": "sucess"}, status=200)

            else:
                # some form errors occured.
                return JsonResponse({"error": form.errors}, status=400)
        else:
            return JsonResponse({"error": ""}, status=400)   
# some error occured    
    return JsonResponse({"error": "aqui"}, status=400)   


   
