from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import TransactionForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .decorators import logout_required
from .models import Profile, Transaction, MarketInfo, UserWallet, ChatMessage
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.db import IntegrityError, transaction
from django.conf import settings
import json

import bitcoinlib
from bitcoinlib.wallets import Wallet
import qrcode
import requests

from PIL import Image
import io
import os

def layout(request):
    form = TransactionForm()
    global_info = MarketInfo.objects.get(id=1)
    user = request.user

    transactions = Transaction.objects.all().order_by('-created_at')

    if user.is_authenticated:

        user_wallet = UserWallet.objects.get(user=request.user)
        wallet_address = user_wallet.wallet_address

        # Generate the QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(wallet_address)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')

        # Save the image to a file in the static directory
        img_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'qr_code.png')
        img.save(img_path)

        # Create a URL for the QR code image
        img_url = '/static/images/qr_code.png'

        # Pass the QR code URL to the template
        context = {
            'form': form,
            'global_info':global_info,
            'transactions': transactions,
            'qr_code': img_url,
        }
    else:
        context = {
            'form': form,
            'global_info':global_info,
            'transactions': transactions,
        }
    return render(request, 'layout.html',context)

@logout_required
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('layout')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})



@logout_required
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                try:
                    user = form.save()
                    # Create the user profile
                    Profile.objects.create(user=user, user_id=user.id)
                    
                    wallet = Wallet.create(user.username)  # Or any custom wallet creation logic
                    
                    wallet_address = wallet.get_key().address
                    private_key = wallet.get_key().wif
                    

                    # Save wallet information
                    UserWallet.objects.create(user=user, wallet_address=wallet_address, private_key=private_key, name = user.username)

                    login(request, user)
                    messages.success(request, "Account created successfully.")

                    return redirect('layout')
                
                except IntegrityError:
                    # Handle integrity errors (e.g., duplicate entries)
                    form.add_error(None, "An error occurred while creating the wallet. Please try again.")
                
                except Exception as e:
                    # Handle other possible exceptions
                    form.add_error(None, f"An unexpected error occurred: {str(e)}")
        else:
            messages.error(request, "Error creating account.")
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('layout')

@login_required
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)

        if form.is_valid():
            amount = form.cleaned_data['amount']
            price = form.cleaned_data['price']

            # Fetch the user's profile or account details (assumed to have balance)
            user_profile = request.user.profile
            
            # Check if the user has sufficient balance
            if user_profile.coins >= amount:
                # Create the transaction record
                u = Transaction.objects.create(
                    user=request.user,
                    amount=amount,
                    price=price
                )

                # Update user's profile (deducting the amount or any other business logic)
                user_profile.coins -= amount
                user_profile.save()


                messages.success(request, 'Transaction completed successfully.')
                return redirect('layout')  # Redirect to some success page or dashboard
            else:
                messages.error(request, 'Insufficient balance.')
        else:
            messages.error(request, 'Invalid data.')
    else:
        form = TransactionForm()

    return redirect('layout')



@login_required
def pull_funds_view(request):
    user_wallet = UserWallet.objects.get(user=request.user)
    wallet_address = user_wallet.wallet_address
    private_key = user_wallet.private_key

    wallet = Wallet(wallet_address)
    balance = wallet.balance()

    # Assuming you have a function to get the balance
    user_wallet_balance = balance

    if request.method == 'POST':

        amount_to_pull = float(request.POST.get('amount'))
        destination_address = request.POST.get('wallet')

        if amount_to_pull > user_wallet_balance:
            messages.error(request, "You don't have enough funds.")
        else:
            try:
                # Create a Bitcoin wallet object using the private key
                wallet = Wallet(private_key=private_key)
                balance = wallet.balance()
                if balance >= amount_to_pull:
                    # Send the amount
                    txid = wallet.send_to(destination_address, amount_to_pull, fee=get_fee_estimate())
                    
                    # Assuming the transaction is successful
                    messages.success(request, f"Successfully sent {amount_to_pull} BTC. Transaction ID: {txid}")
                    return redirect(layout)
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")

    return redirect(layout)



def get_fee_estimate():
    try:
        # Request the fee estimates from mempool.space API
        response = requests.get("https://mempool.space/api/v1/fees/recommended")
        response.raise_for_status()  # Raise an error for bad responses

        # Extract the fee rates from the response
        fees = response.json()
        #fastest_fee = fees['fastestFee']  # Satoshis per byte
        half_hour_fee = fees['halfHourFee']  # Satoshis per byte
        #hour_fee = fees['hourFee']  # Satoshis per byte

        return half_hour_fee

    except requests.RequestException as e:
        print(f"Error fetching fee estimate: {e}")
        return None


@login_required
def create_coin(request):
    # Check if the request method is POST
    if request.method == 'POST':
        buy_amount = float(request.POST.get('amount'))
        user = Profile.objects.get(user=request.user)
        try:
            market_info = MarketInfo.objects.get(id=1)
            print(buy_amount * market_info.price)
            if buy_amount * market_info.price <= user.btc :
                user.btc =- buy_amount * MarketInfo.price
                user.coins += buy_amount
                print(user.coins)
                user.save()
            # Assuming the purchase was successful
            messages.success(request, f"Successfully purchased .")
            return redirect('layout')  # Redirect to the money transfer page or wherever appropriate

        except Exception as e:
            # Handle any exceptions that occur during the purchase
            messages.error(request, f"An error occurred while buying coins: {str(e)}")
            return redirect('layout')

    # If the request is not POST, just redirect to the money transfer page
    return redirect('layout')


@csrf_exempt
@require_POST
def buy_transaction(request):
    data = json.loads(request.body)
    transaction_id = data.get('id')
    
    if not transaction_id:
        return JsonResponse({'error': 'Transaction ID is required.'}, status=400)

    try:

        transaction = Transaction.objects.get(id=transaction_id)
        transaction_price = transaction.price
        transaction_amount = transaction.amount
        Seller = transaction.user

        Buyer = request.user

        Seller_prof = Profile.objects.get(user=Seller)
        Buyer_prof = Profile.objects.get(user=request.user)
        
        if Buyer_prof.money >= transaction_amount*transaction_price:
            Seller_prof.coins -= transaction_amount
            Buyer_prof.coins += transaction_amount

            Seller_prof.money += transaction_amount*transaction_price
            Buyer_prof.money -= transaction_amount*transaction_price

            
            transaction.delete()
            Seller_prof.save()
            Buyer_prof.save()


            # Perform the purchase logic here
            # For example, mark the transaction as bought or process the payment

            # Dummy response for the sake of example
            return redirect('layout')
        return redirect('layout')
    except Transaction.DoesNotExist:
        return JsonResponse({'error': 'Transaction not found.'}, status=404)
  

def get_ajax_info(request):
    
    transactions = list(Transaction.objects.all().order_by('-created_at').values(
        'created_at', 'user__username', 'amount', 'price', 'id'
    ))

    # Get chat messages ordered by created_at
    messages = list(ChatMessage.objects.all().order_by('-created_at').values(
        'user__username', 'message', 'created_at', 'id'
    ))

    def get_btc_to_usd():
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': 'bitcoin',
            'vs_currencies': 'usd'
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an error for bad status codes
            data = response.json()
            btc_to_usd_rate = data['bitcoin']['usd']

            market = MarketInfo.objects.get(id=1)
            market.btc_price = btc_to_usd_rate
            market.save()

            return btc_to_usd_rate
        except requests.exceptions.RequestException as e:
            print(f"Error fetching BTC to USD conversion rate: {e}")
            return None
    
    
    User_req = request.user
    name = request.user.username
    if User_req.is_authenticated:

        user_prof = Profile.objects.get(user_id = User_req.id)
        wallet = UserWallet.objects.get(user = user_prof.user)
        
        try:
            
            # Load the wallet using the key
            wallet = Wallet(wallet.name)

            # Get the wallet balance
            balance = wallet.balance()

            # Print the balance
            
        except Exception as e:
            
            balance=0.000000000069420
            

        user__username = user_prof.user.username 
        coins = user_prof.coins
        money=user_prof.money
        btc = balance
        profit = user_prof.profit
        user_info = {
            'user__username': user__username , 
            'coins':coins, 
            'money':money, 
            'btc': btc,
            'profit':profit
        }

        data = {
        'transactions': transactions,
        'messages': messages,
        'user_info':  user_info 
        }
    
    else:
    # Combine both lists into a dictionary
        data = {
            'transactions': transactions,
            'messages': messages
        }

    return JsonResponse(data)
        
    


@csrf_exempt
@login_required
def create_message(request):
    if request.method == 'POST':
        message = request.POST.get('chat-input')
        if len(message)<100:
            user = request.user
            ChatMessage.objects.create(user=request.user, message=message)
            return redirect(layout)
        
    return redirect(layout)