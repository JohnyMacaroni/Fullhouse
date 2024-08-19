import bitcoinlib
from bitcoinlib.wallets import Wallet

wallet = Wallet()

# Get the wallet balance
balance = wallet.balance()

print(balance)
print(wallet)