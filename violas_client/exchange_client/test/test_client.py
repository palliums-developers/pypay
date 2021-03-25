from violas_client.exchange_client import Wallet, Client
from violas_client.move_core_types.language_storage import core_code_address

module_address = "00000000000000000000000045584348"

client = Client("violas_testnet")
client.set_exchange_module_address(core_code_address())
client.set_exchange_owner_address(module_address)

def test_add_liquidity():
    wallet = Wallet.new()

    liquidity_account = wallet.new_account()
    client.mint_coin(liquidity_account.address, 10_000_000, auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True, currency_code="vUSDT")
    client.add_currency_to_account(liquidity_account, "vBTC")
    client.mint_coin(liquidity_account.address, 10_000_000, currency_code="vBTC", auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True)

    swap_account = wallet.new_account()
    client.mint_coin(swap_account.address, 10_000_000, auth_key_prefix=swap_account.auth_key_prefix, is_blocking=True, currency_code="vUSDT")
    client.add_currency_to_account(swap_account, "vBTC")
    client.mint_coin(swap_account.address, 10_000_000, currency_code="vBTC", auth_key_prefix=swap_account.auth_key_prefix, is_blocking=True)

    vUSDT_before_balance = client.get_balance(liquidity_account.address, "vUSDT")
    vBTC_before_balance = client.get_balance(liquidity_account.address, "vBTC")
    client.swap_add_liquidity(liquidity_account, "vUSDT", "vBTC", 1_000_000, 321_432)
    vUSDT_after_balance = client.get_balance(liquidity_account.address, "vUSDT")
    vBTC_after_balance = client.get_balance(liquidity_account.address, "vBTC")
    assert vUSDT_before_balance - vUSDT_after_balance == 1_000_000 or vBTC_before_balance - vBTC_after_balance == 321_432

def test_remove_liquidity():
    wallet = Wallet.new()

    liquidity_account = wallet.new_account()
    client.mint_coin(liquidity_account.address, 10_000_000, auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True, currency_code="vUSDT")
    client.add_currency_to_account(liquidity_account, "vBTC")
    client.mint_coin(liquidity_account.address, 10_000_000, currency_code="vBTC", auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True)

    swap_account = wallet.new_account()
    client.mint_coin(swap_account.address, 10_000_000, auth_key_prefix=swap_account.auth_key_prefix, is_blocking=True, currency_code="vUSDT")
    client.add_currency_to_account(swap_account, "vBTC")
    client.mint_coin(swap_account.address, 10_000_000, currency_code="vBTC", auth_key_prefix=swap_account.auth_key_prefix, is_blocking=True)

    client.swap_add_liquidity(liquidity_account, "vUSDT", "vBTC", 1_000_000, 321_432)
    values = client.swap_get_liquidity_balances(liquidity_account.address)[0]
    client.swap_remove_liquidity(liquidity_account, "vBTC", "vUSDT", values["liquidity"])

def test_swap():
    wallet = Wallet.new()

    liquidity_account = wallet.new_account()
    client.mint_coin(liquidity_account.address, 10_000_000, auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True, currency_code="vUSDT")
    client.add_currency_to_account(liquidity_account, "vBTC")
    client.mint_coin(liquidity_account.address, 10_000_000, currency_code="vBTC", auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True)

    swap_account = wallet.new_account()
    client.mint_coin(swap_account.address, 10_000_000, auth_key_prefix=swap_account.auth_key_prefix, is_blocking=True, currency_code="vUSDT")
    client.add_currency_to_account(swap_account, "vBTC")
    client.mint_coin(swap_account.address, 10_000_000, currency_code="vBTC", auth_key_prefix=swap_account.auth_key_prefix, is_blocking=True)

    client.swap_add_liquidity(liquidity_account, "vUSDT", "vBTC", 123_321, 321_432)

    (expected_amount, out) = client.swap_get_swap_output_amount("vBTC", "vUSDT", 1000)
    before_amount = client.get_balance(swap_account.address, "vUSDT")
    client.swap(swap_account, "vBTC", "vUSDT", 1000, expected_amount)
    after_amount = client.get_balance(swap_account.address, "vUSDT")
    assert after_amount - before_amount == expected_amount


def test_swap_get_liquidity_balances():
    wallet = Wallet.new()

    liquidity_account = wallet.new_account()
    client.mint_coin(liquidity_account.address, 10_000_000, auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True, currency_code="vUSDT")
    client.add_currency_to_account(liquidity_account, "vBTC")
    client.mint_coin(liquidity_account.address, 10_000_000, currency_code="vBTC", auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True)
    client.add_currency_to_account(liquidity_account, "VLS")

    swap_account = wallet.new_account()
    client.mint_coin(swap_account.address, 10_000_000, auth_key_prefix=swap_account.auth_key_prefix, is_blocking=True, currency_code="vUSDT")
    client.add_currency_to_account(swap_account, "vBTC")
    client.mint_coin(swap_account.address, 10_000_000, currency_code="vBTC", auth_key_prefix=swap_account.auth_key_prefix,is_blocking=True)

    client.swap_add_liquidity(liquidity_account, "vUSDT", "vBTC", 2344532, 342566)
    client.swap(swap_account, "vBTC", "vUSDT", 1000)
    blb = client.get_balance(liquidity_account.address, "vUSDT")
    bc1b = client.get_balance(liquidity_account.address, "vBTC")
    all = client.swap_get_liquidity_balances(liquidity_account.address)[0]
    client.swap_remove_liquidity(liquidity_account, "vBTC", "vUSDT", all["liquidity"])
    alb = client.get_balance(liquidity_account.address, "vUSDT")
    ac1b = client.get_balance(liquidity_account.address, "vBTC")
    assert alb - blb == all["vUSDT"]
    assert ac1b - bc1b == all["vBTC"]

def test_swap_get_swap_output_amount():
    wallet = Wallet.new()

    liquidity_account = wallet.new_account()
    client.mint_coin(liquidity_account.address, 10_000_000, auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True, currency_code="vUSDT")
    client.add_currency_to_account(liquidity_account, "vBTC")
    client.mint_coin(liquidity_account.address, 10_000_000, currency_code="vBTC",auth_key_prefix=liquidity_account.auth_key_prefix,is_blocking=True)

    swap_account = wallet.new_account()
    client.mint_coin(swap_account.address, 10_000_000, auth_key_prefix=swap_account.auth_key_prefix,is_blocking=True, currency_code="vUSDT")
    client.add_currency_to_account(swap_account, "vBTC")
    client.mint_coin(swap_account.address, 10_000_000, currency_code="vBTC",auth_key_prefix=swap_account.auth_key_prefix,is_blocking=True)

    client.swap_add_liquidity(liquidity_account, "vUSDT", "vBTC", 342423, 435435)
    out, _ = client.swap_get_swap_output_amount("vBTC", "vUSDT", 100_000)
    bb = client.get_balance(swap_account.address, "vUSDT")
    client.swap(swap_account, "vBTC", "vUSDT", 100_000)
    ab = client.get_balance(swap_account.address, "vUSDT")
    assert ab - bb == out

def test_swap_get_swap_input_amount():
    wallet = Wallet.new()

    liquidity_account = wallet.new_account()
    client.mint_coin(liquidity_account.address, 10_000_000, auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True, currency_code="vUSDT")
    client.add_currency_to_account(liquidity_account, "vBTC")
    client.mint_coin(liquidity_account.address, 10_000_000, currency_code="vBTC",auth_key_prefix=liquidity_account.auth_key_prefix,is_blocking=True)

    swap_account = wallet.new_account()
    client.mint_coin(swap_account.address, 10_000_000, auth_key_prefix=swap_account.auth_key_prefix,is_blocking=True, currency_code="vUSDT")
    client.add_currency_to_account(swap_account, "vBTC")
    client.mint_coin(swap_account.address, 10_000_000, currency_code="vBTC",auth_key_prefix=swap_account.auth_key_prefix,is_blocking=True)

    client.swap_add_liquidity(liquidity_account, "vUSDT", "vBTC", 3243244, 4354435)
    out, _ = client.swap_get_swap_input_amount("vBTC", "vUSDT", 243444)
    bb = client.get_balance(swap_account.address, "vUSDT")
    client.swap(swap_account, "vBTC", "vUSDT", out)
    ab = client.get_balance(swap_account.address, "vUSDT")
    assert 243444-1 <= ab - bb <= 243444+1

def test_swap_get_liquidity_output_amount():
    wallet = Wallet.new()

    liquidity_account = wallet.new_account()
    client.mint_coin(liquidity_account.address, 10_000_000, auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True, currency_code="vUSDT")
    client.add_currency_to_account(liquidity_account, "vBTC")
    client.mint_coin(liquidity_account.address, 10_000_000, currency_code="vBTC",auth_key_prefix=liquidity_account.auth_key_prefix,is_blocking=True)
    client.add_currency_to_account(liquidity_account, "VLS")

    swap_account = wallet.new_account()
    client.mint_coin(swap_account.address, 10_000_000, auth_key_prefix=swap_account.auth_key_prefix,is_blocking=True, currency_code="vUSDT")
    client.add_currency_to_account(swap_account, "vBTC")
    client.mint_coin(swap_account.address, 10_000_000, currency_code="vBTC",auth_key_prefix=swap_account.auth_key_prefix,is_blocking=True)

    client.swap_add_liquidity(liquidity_account, "vUSDT", "vBTC", 3243243, 432432)
    out = client.swap_get_liquidity_output_amount("vBTC", "vUSDT", 243244)
    bc1b = client.get_balance(liquidity_account.address, "vBTC")
    client.swap_add_liquidity(liquidity_account, "vUSDT", "vBTC", out, 1000000000)
    ac1b = client.get_balance(liquidity_account.address, "vBTC")
    assert bc1b - ac1b == 243244

def test_withdraw_mine_reward():
    import time
    wallet = Wallet.new()
    client = Client()
    liquidity_account = wallet.new_account()
    client.mint_coin(liquidity_account.address, 10_000_000, currency_code="vBTC",
                     auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True)
    client.add_currency_to_account(liquidity_account, "vUSDT")

    client.mint_coin(liquidity_account.address, 10_000_000, currency_code="vUSDT",
                     auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True)
    client.add_currency_to_account(liquidity_account, "VLS")

    client.swap_add_liquidity(liquidity_account, "vBTC", "vUSDT", 200_000, 100_000)
    time.sleep(1)
    amount = client.swap_get_reward_balance(liquidity_account.address_hex)
    seq = client.swap_withdraw_mine_reward(liquidity_account)
    tx = client.get_account_transaction(liquidity_account.address_hex, seq)
    assert amount == tx.get_swap_reward_amount()


