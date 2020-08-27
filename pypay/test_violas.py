# violas test
# addr: 34a1a1b8e159193a524bb26f40e8eacf

from violas_client import Wallet, Client

#wallet = Wallet.new()
wallet = Wallet.new_from_mnemonic("exercise kitchen spawn catalog hair intact shrimp stem version flee ozone exhibit")
mnemonic = wallet.mnemonic
print("mnemonic: ", mnemonic)

account = wallet.new_account()
address = wallet.accounts[0].address_hex
print("address: ", address)

client = Client()
balance = client.get_balance(account.address, "LBR")
print("balance: ", balance)

'''
client.mint_coin(account.address, 10_000_000, auth_key_prefix=account.auth_key_prefix, is_blocking=True)
balance = client.get_balance(account.address, "LBR")
print("balance: ", balance)
'''


client.mint_coin(account.address, 10_000_000, auth_key_prefix=account.auth_key_prefix, is_blocking=True, currency_code="VLSUSD")
client.transfer_coin(account, '332c87f481f1180a34410d795d12cf9d', 100, currency_code='VLSUSD')
