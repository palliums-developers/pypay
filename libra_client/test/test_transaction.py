from libra_client.lbrtypes.account_config import testnet_dd_account_address
from libra_client import Client, Wallet
from typing import List
from libra_client.account import Account

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

def test_get_sender():
    client = create_client()
    [a1, a2] = create_accounts(2)
    seq = client.mint_coin(a1.address, 100, auth_key_prefix=a1.auth_key_prefix, is_blocking=True)
    tx = client.get_account_transaction(testnet_dd_account_address(), seq)
    assert tx.get_sender() == testnet_dd_account_address().hex().lower()

    seq = client.mint_coin(a2.address, 100, auth_key_prefix=a2.auth_key_prefix, is_blocking=True)
    seq = client.transfer_coin(a1, a2.address, 10, is_blocking=True)
    tx = client.get_account_transaction(a1.address, seq)
    assert tx.get_sender() == a1.address_hex.lower()

    tx = client.get_transaction(0)
    assert None == tx.get_sender()

    tx = client.get_transaction(1)
    assert None == tx.get_sender()

def test_get_receiver():
    client = create_client()
    [a1, a2] = create_accounts(2)
    seq = client.mint_coin(a1.address, 100, auth_key_prefix=a1.auth_key_prefix, is_blocking=True)
    tx = client.get_account_transaction(testnet_dd_account_address(), seq)
    assert tx.get_receiver() == a1.address_hex.lower()

    seq = client.mint_coin(a2.address, 100, auth_key_prefix=a2.auth_key_prefix, is_blocking=True)
    seq = client.transfer_coin(a1, a2.address, 10, is_blocking=True)
    tx = client.get_account_transaction(a1.address, seq)
    assert tx.get_receiver() == a2.address_hex.lower()

    tx = client.get_transaction(0)
    assert None == tx.get_receiver()

    tx = client.get_transaction(1)
    assert None == tx.get_receiver()

def test_get_amount():
    client = create_client()
    [a1, a2] = create_accounts(2)
    seq = client.mint_coin(a1.address, 99, auth_key_prefix=a1.auth_key_prefix, is_blocking=True)
    tx = client.get_account_transaction(testnet_dd_account_address(), seq)
    assert tx.get_amount() == 99

    seq = client.mint_coin(a2.address, 100, auth_key_prefix=a2.auth_key_prefix, is_blocking=True)
    seq = client.transfer_coin(a1, a2.address, 88, is_blocking=True)
    tx = client.get_account_transaction(a1.address, seq)
    assert tx.get_amount() == 88

    tx = client.get_transaction(0)
    assert None == tx.get_amount()

    tx = client.get_transaction(1)
    assert None == tx.get_amount()

def test_get_currency_code():
    client = create_client()
    [a1, a2] = create_accounts(2)
    seq = client.mint_coin(a1.address, 99, auth_key_prefix=a1.auth_key_prefix, is_blocking=True)
    tx = client.get_account_transaction(testnet_dd_account_address(), seq)
    assert tx.get_currency_code() == "XUS"

    seq = client.mint_coin(a2.address, 100, auth_key_prefix=a2.auth_key_prefix, is_blocking=True)
    seq = client.transfer_coin(a1, a2.address, 88, is_blocking=True)
    tx = client.get_account_transaction(a1.address, seq)
    assert tx.get_currency_code() == "XUS"

    tx = client.get_transaction(0)
    assert None == tx.get_currency_code()

    tx = client.get_transaction(1)
    assert None == tx.get_currency_code()

def test_get_data():
    client = create_client()
    [a1, a2] = create_accounts(2)
    seq = client.mint_coin(a1.address, 100, auth_key_prefix=a1.auth_key_prefix, is_blocking=True)
    tx = client.get_account_transaction(testnet_dd_account_address(), seq)
    assert tx.get_data() == ""

    data = b"data"
    seq = client.mint_coin(a2.address, 100, auth_key_prefix=a2.auth_key_prefix, is_blocking=True)
    seq = client.transfer_coin(a1, a2.address, 10, is_blocking=True, data=data)
    tx = client.get_account_transaction(a1.address, seq)
    assert tx.get_data() == data.hex()

    seq = client.transfer_coin(a1, a2.address, 10,  is_blocking=True)
    tx = client.get_account_transaction(a1.address, seq)
    assert tx.get_data() == ""

    tx = client.get_transaction(0)
    assert None == tx.get_data()

    tx = client.get_transaction(1)
    assert None == tx.get_data()