from violas_client import Client, Wallet
from violas_client.move_core_types.language_storage import core_code_address

import time

client = Client("violas_testnet")

def approximately_equal_to(a, b):
    a = int(a)
    b = int(b)
    return a in range(b-5, b+5)

def test_get_total_collateral_value():
    wallet = Wallet.new()
    a1 = wallet.new_account()
    client.mint_coin(a1.address, 300_000_000, auth_key_prefix=a1.auth_key_prefix, currency_code="vBTC")
    client.bank_publish(a1)
    client.mint_coin(a1.address, 300_000_000, auth_key_prefix=a1.auth_key_prefix, currency_code="vBTC")
    client.bank_lock2(a1, 100_000_000, currency_code="vBTC")
    # assert approximately_equal_to(client.bank_get_total_collateral_value(a1.address), 100_000_000 / 2)

def test_get_total_borrow_value():
    wallet = Wallet.new()
    a1 = wallet.new_account()
    client.mint_coin(a1.address, 300_000_000, auth_key_prefix=a1.auth_key_prefix, currency_code="vBTC")
    client.bank_publish(a1, gas_currency_code="vBTC")
    client.bank_lock2(a1, 100_000_000, currency_code="vBTC")
    client.bank_borrow2(a1, 10_000_000, currency_code="vBTC")
    # assert approximately_equal_to(client.bank_get_total_borrow_value(a1.address), 10_000_000)

def test_get_max_borrow_amount():
    wallet = Wallet.new()
    a1 = wallet.new_account()
    client.mint_coin(a1.address, 300_000_000, auth_key_prefix=a1.auth_key_prefix, currency_code="vBTC")
    client.bank_publish(a1, gas_currency_code="vBTC")
    client.bank_lock2(a1, 100_000_000, currency_code="vBTC")
    client.bank_borrow2(a1, 10_000_000, currency_code="vBTC")
    assert approximately_equal_to(client.bank_get_max_borrow_amount(a1.address, "vBTC"), 40_000_000)

def test_lock():
    wallet = Wallet.new()
    a1 = wallet.new_account()
    client.mint_coin(a1.address, 300_000_000, auth_key_prefix=a1.auth_key_prefix, currency_code="vBTC")
    client.bank_publish(a1)
    client.mint_coin(a1.address, 300_000_000, auth_key_prefix=a1.auth_key_prefix, currency_code="vBTC")
    client.bank_lock2(a1, 100_000_000, currency_code="vBTC")
    assert approximately_equal_to(client.bank_get_lock_amount(a1.address, currency_code="vBTC"), 100_000_000)

def test_redeem():
    wallet = Wallet.new()
    a1 = wallet.new_account()
    client.mint_coin(a1.address, 300_000_000, auth_key_prefix=a1.auth_key_prefix, currency_code="vBTC")
    client.bank_publish(a1, gas_currency_code="vBTC")
    client.bank_lock2(a1, 100_000_000, currency_code="vBTC")
    amount = client.bank_get_lock_amount(a1.address, "vBTC")
    client.bank_redeem2(a1, amount=amount, currency_code="vBTC")
    assert approximately_equal_to(client.get_balance(a1.address, currency_code="vBTC"), 300_000_000)

def test_borrow():
    wallet = Wallet.new()
    a1 = wallet.new_account()
    client.mint_coin(a1.address, 300_000_000, auth_key_prefix=a1.auth_key_prefix, currency_code="vBTC")
    client.bank_publish(a1, gas_currency_code="vBTC")
    client.bank_lock2(a1, 100_000_000, currency_code="vBTC")
    client.bank_borrow2(a1, 40_000_000, currency_code="vBTC")
    assert approximately_equal_to(client.bank_get_borrow_amount(a1.address, currency_code="vBTC")[1], 40_000_000)

def test_repay_borrow():
    wallet = Wallet.new()
    a1 = wallet.new_account()
    client.mint_coin(a1.address, 300_000_000, auth_key_prefix=a1.auth_key_prefix, currency_code="vBTC")
    client.bank_publish(a1)
    client.bank_lock2(a1, 200_000_000, currency_code="vBTC")
    client.bank_borrow2(a1, 10_000_000, currency_code="vBTC")
    _, amount = client.bank_get_borrow_amount(a1.address, "vBTC")
    client.add_currency_to_account(a1, "VLS")
    client.bank_repay_borrow2(a1, currency_code="vBTC", amount=amount)
    assert client.bank_get_borrow_amount(a1.address, currency_code="vBTC")[0] == 0

def test_bank_get_supply_rate():
    wallet = Wallet.new()
    a1 = wallet.new_account()
    a2 = wallet.new_account()
    client.mint_coin(a1.address, 300_000_000, auth_key_prefix=a1.auth_key_prefix, currency_code="vBTC")
    client.mint_coin(a2.address, 300_000_000, auth_key_prefix=a2.auth_key_prefix, currency_code="vBTC")
    client.bank_publish(a1)
    client.bank_publish(a2)
    client.bank_lock2(a1, 100_000_000, currency_code="vBTC")
    client.bank_borrow2(a1, 10_000_000, currency_code="vBTC")
    client.bank_lock2(a2, 100_000_000, currency_code="vBTC")
    lock_rate = client.bank_get_lock_rate("vBTC")
    time.sleep(60)
    lock_amount = client.bank_get_lock_amount(a2.address, currency_code="vBTC")
    assert approximately_equal_to(lock_amount, 100_000_000 + 100_000_000*lock_rate)
    client.add_currency_to_account(a2, "VLS")
    client.bank_redeem2(a2, amount=lock_amount, currency_code="vBTC")
    assert approximately_equal_to(client.bank_get_lock_amount(a2.address, "vBTC"), 0)

def test_bank_get_borrow_rate():
    wallet = Wallet.new()
    a1 = wallet.new_account()
    client.mint_coin(a1.address, 300_000_000, auth_key_prefix=a1.auth_key_prefix, currency_code="vBTC")
    client.bank_publish(a1)
    client.bank_lock2(a1, 100_000_000, currency_code="vBTC")
    client.bank_borrow2(a1, 10_000_000, currency_code="vBTC")
    borrow_rate = client.bank_get_borrow_rate(currency_code="vBTC")
    time.sleep(120)
    client.add_currency_to_account(a1, "VLS")
    _, borrow_amount = client.bank_get_borrow_amount(a1.address, currency_code="vBTC")
    assert approximately_equal_to(borrow_amount, 10_000_000+10_000_000*borrow_rate*2)
    client.bank_repay_borrow2(a1, amount=borrow_amount, currency_code="vBTC")
    assert client.bank_get_borrow_amount(a1.address, "vBTC")[0] == 0

def test_liquidate_borrow():
    wallet = Wallet.new()
    a1 = wallet.new_account()
    client.mint_coin(a1.address, 300_000_000_000, auth_key_prefix=a1.auth_key_prefix, currency_code="vBTC")
    client.bank_publish(a1, gas_currency_code="vBTC")
    client.bank_lock2(a1, 100_000_000_000, currency_code="vBTC")
    client.bank_borrow2(a1, 50_000_000_000-100, currency_code="vBTC")

def test_get_sum_incentive_amount():
    wallet = Wallet.new()
    module_account = wallet.new_account()
    client.mint_coin(module_account.address, 200_000_000, auth_key_prefix=module_account.auth_key_prefix,
                     currency_code="vBTC")
    client.bank_publish(module_account)
    a1 = wallet.new_account()
    client.mint_coin(a1.address, 300_000_000, auth_key_prefix=a1.auth_key_prefix, currency_code="vBTC")
    client.bank_publish(a1)
    client.add_currency_to_account(a1, "VLS")
    client.bank_lock2(a1, 100_000_000, currency_code="vBTC")
    time.sleep(60)
    amount = client.bank_get_sum_incentive_amount(a1.address_hex)
    seq = client.bank_redeem2(a1, 100_000_000, currency_code="vBTC")
    tx = client.get_account_transaction(a1.address_hex, seq)
    assert tx.get_incentive() == amount
