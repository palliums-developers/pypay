# libra test

from libra_client import Wallet, Client

wallet = Wallet.new()
mnemonic = wallet.mnemonic
print(mnemonic)
account = wallet.new_account()
address = wallet.accounts[0].address_hex
print(address)
