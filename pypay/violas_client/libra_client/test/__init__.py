from violas_client.libra_client import Client, Wallet
from typing import List
from violas_client.libra_client.account import Account

def create_accounts(account_number)-> List[Account]:
    wallet = Wallet.new()
    return [wallet.new_account() for _ in range(account_number)]

def create_accounts_with_coins(account_number)-> List[Account]:
    wallet = Wallet.new()
    client = create_client()
    accounts = []
    for _ in range(account_number):
        account = wallet.new_account()
        client.mint_coin(account.address, 100, auth_key_prefix=account.auth_key_prefix, is_blocking=True)
        accounts.append(account)
    return accounts

def create_client() -> Client:
    return Client()