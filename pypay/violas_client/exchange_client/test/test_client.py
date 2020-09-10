from violas_client.exchange_client import Wallet, Client
from violas_client.move_core_types.language_storage import core_code_address

module_address = "00000000000000000000000045584348"

client = Client()
client.set_exchange_module_address(core_code_address())
client.set_exchange_owner_address(module_address)

def test_add_liquidity():
    wallet = Wallet.new()

    liquidity_account = wallet.new_account()
    client.mint_coin(liquidity_account.address, 10_000_000, auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True, currency_code="USD")
    client.add_currency_to_account(liquidity_account, "EUR")
    client.mint_coin(liquidity_account.address, 10_000_000, currency_code="EUR", auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True)

    swap_account = wallet.new_account()
    client.mint_coin(swap_account.address, 10_000_000, auth_key_prefix=swap_account.auth_key_prefix, is_blocking=True)
    client.add_currency_to_account(swap_account, "EUR")
    client.mint_coin(swap_account.address, 10_000_000, currency_code="EUR", auth_key_prefix=swap_account.auth_key_prefix, is_blocking=True)

    USD_before_balance = client.get_balance(liquidity_account.address, "USD")
    EUR_before_balance = client.get_balance(liquidity_account.address, "EUR")
    client.swap_add_liquidity(liquidity_account, "USD", "EUR", 1_000_000, 321_432)
    USD_after_balance = client.get_balance(liquidity_account.address, "USD")
    EUR_after_balance = client.get_balance(liquidity_account.address, "EUR")
    assert USD_before_balance - USD_after_balance == 1_000_000 or EUR_before_balance - EUR_after_balance == 321_432


def test_remove_liquidity():
    wallet = Wallet.new()

    liquidity_account = wallet.new_account()
    client.mint_coin(liquidity_account.address, 10_000_000, auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True, currency_code="USD")
    client.add_currency_to_account(liquidity_account, "EUR")
    client.mint_coin(liquidity_account.address, 10_000_000, currency_code="EUR", auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True)

    swap_account = wallet.new_account()
    client.mint_coin(swap_account.address, 10_000_000, auth_key_prefix=swap_account.auth_key_prefix, is_blocking=True)
    client.add_currency_to_account(swap_account, "EUR")
    client.mint_coin(swap_account.address, 10_000_000, currency_code="EUR", auth_key_prefix=swap_account.auth_key_prefix, is_blocking=True)

    client.swap_add_liquidity(liquidity_account, "USD", "EUR", 1_000_000, 321_432)
    values = client.swap_get_liquidity_balances(liquidity_account.address)[0]
    client.swap_remove_liquidity(liquidity_account, "EUR", "USD", values["liquidity"])

def test_swap():
    wallet = Wallet.new()

    liquidity_account = wallet.new_account()
    client.mint_coin(liquidity_account.address, 10_000_000, auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True, currency_code="USD")
    client.add_currency_to_account(liquidity_account, "EUR")
    client.mint_coin(liquidity_account.address, 10_000_000, currency_code="EUR", auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True)
    client.add_currency_to_account(liquidity_account, "GBP")
    client.mint_coin(liquidity_account.address, 10_000_000, currency_code="GBP", auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True)

    swap_account = wallet.new_account()
    client.mint_coin(swap_account.address, 10_000_000, auth_key_prefix=swap_account.auth_key_prefix, is_blocking=True, currency_code="USD")
    client.add_currency_to_account(swap_account, "EUR")
    client.mint_coin(swap_account.address, 10_000_000, currency_code="EUR", auth_key_prefix=swap_account.auth_key_prefix, is_blocking=True)
    client.add_currency_to_account(swap_account, "GBP")
    client.mint_coin(swap_account.address, 10_000_000, currency_code="GBP", auth_key_prefix=swap_account.auth_key_prefix, is_blocking=True)

    client.swap_add_liquidity(liquidity_account, "USD", "EUR", 123_321, 321_432)
    client.swap_add_liquidity(liquidity_account, "GBP", "EUR", 321_432, 321_432)

    (expected_amount, out) = client.swap_get_swap_output_amount("EUR", "USD", 1000)
    before_amount = client.get_balance(swap_account.address, "USD")
    client.swap(swap_account, "EUR", "USD", 1000, expected_amount)
    after_amount = client.get_balance(swap_account.address, "USD")
    assert after_amount - before_amount == expected_amount

    (expected_amount, out) = client.swap_get_swap_output_amount("EUR", "USD", 1000)
    before_amount = client.get_balance(liquidity_account.address, "USD")
    client.swap(swap_account, "EUR", "USD", 1000, expected_amount, receiver_address=liquidity_account.address)
    after_amount = client.get_balance(liquidity_account.address, "USD")
    assert after_amount - before_amount == expected_amount

def test_swap_get_liquidity_balances():
    wallet = Wallet.new()

    liquidity_account = wallet.new_account()
    client.mint_coin(liquidity_account.address, 10_000_000, auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True, currency_code="USD")
    client.add_currency_to_account(liquidity_account, "EUR")
    client.mint_coin(liquidity_account.address, 10_000_000, currency_code="EUR", auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True)
    client.add_currency_to_account(liquidity_account, "GBP")
    client.mint_coin(liquidity_account.address, 10_000_000, currency_code="GBP", auth_key_prefix=liquidity_account.auth_key_prefix,is_blocking=True)

    swap_account = wallet.new_account()
    client.mint_coin(swap_account.address, 10_000_000, auth_key_prefix=swap_account.auth_key_prefix, is_blocking=True, currency_code="USD")
    client.add_currency_to_account(swap_account, "EUR")
    client.mint_coin(swap_account.address, 10_000_000, currency_code="EUR", auth_key_prefix=swap_account.auth_key_prefix,is_blocking=True)
    client.add_currency_to_account(swap_account, "GBP")
    client.mint_coin(swap_account.address, 10_000_000, currency_code="GBP", auth_key_prefix=swap_account.auth_key_prefix, is_blocking=True)

    client.swap_add_liquidity(liquidity_account, "USD", "EUR", 2344532, 342566)
    client.swap_add_liquidity(liquidity_account, "USD", "EUR", 5324232, 323435)
    client.swap(swap_account, "EUR", "USD", 1000)
    blb = client.get_balance(liquidity_account.address, "USD")
    bc1b = client.get_balance(liquidity_account.address, "EUR")
    all = client.swap_get_liquidity_balances(liquidity_account.address)[0]
    client.swap_remove_liquidity(liquidity_account, "EUR", "USD", all["liquidity"])
    alb = client.get_balance(liquidity_account.address, "USD")
    ac1b = client.get_balance(liquidity_account.address, "EUR")
    assert alb - blb == all["USD"]
    assert ac1b - bc1b == all["EUR"]

def test_swap_get_swap_output_amount():
    wallet = Wallet.new()

    liquidity_account = wallet.new_account()
    client.mint_coin(liquidity_account.address, 10_000_000, auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True, currency_code="USD")
    client.add_currency_to_account(liquidity_account, "EUR")
    client.mint_coin(liquidity_account.address, 10_000_000, currency_code="EUR",auth_key_prefix=liquidity_account.auth_key_prefix,is_blocking=True)
    client.add_currency_to_account(liquidity_account, "GBP")
    client.mint_coin(liquidity_account.address, 10_000_000, currency_code="GBP",auth_key_prefix=liquidity_account.auth_key_prefix,is_blocking=True)

    swap_account = wallet.new_account()
    client.mint_coin(swap_account.address, 10_000_000, auth_key_prefix=swap_account.auth_key_prefix,is_blocking=True, currency_code="USD")
    client.add_currency_to_account(swap_account, "EUR")
    client.mint_coin(swap_account.address, 10_000_000, currency_code="EUR",auth_key_prefix=swap_account.auth_key_prefix,is_blocking=True)
    client.add_currency_to_account(swap_account, "GBP")
    client.mint_coin(swap_account.address, 10_000_000, currency_code="GBP",auth_key_prefix=swap_account.auth_key_prefix,is_blocking=True)

    client.swap_add_liquidity(liquidity_account, "USD", "EUR", 342423, 435435)
    client.swap_add_liquidity(liquidity_account, "GBP", "EUR", 453452, 243244)
    out, _ = client.swap_get_swap_output_amount("GBP", "USD", 100_000)
    bb = client.get_balance(swap_account.address, "USD")
    client.swap(swap_account, "GBP", "USD", 100_000)
    ab = client.get_balance(swap_account.address, "USD")
    assert ab - bb == out

def test_swap_get_swap_input_amount():
    wallet = Wallet.new()

    liquidity_account = wallet.new_account()
    client.mint_coin(liquidity_account.address, 10_000_000, auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True, currency_code="USD")
    client.add_currency_to_account(liquidity_account, "EUR")
    client.mint_coin(liquidity_account.address, 10_000_000, currency_code="EUR",auth_key_prefix=liquidity_account.auth_key_prefix,is_blocking=True)
    client.add_currency_to_account(liquidity_account, "GBP")
    client.mint_coin(liquidity_account.address, 10_000_000, currency_code="GBP",auth_key_prefix=liquidity_account.auth_key_prefix,is_blocking=True)

    swap_account = wallet.new_account()
    client.mint_coin(swap_account.address, 10_000_000, auth_key_prefix=swap_account.auth_key_prefix,is_blocking=True, currency_code="USD")
    client.add_currency_to_account(swap_account, "EUR")
    client.mint_coin(swap_account.address, 10_000_000, currency_code="EUR",auth_key_prefix=swap_account.auth_key_prefix,is_blocking=True)
    client.add_currency_to_account(swap_account, "GBP")
    client.mint_coin(swap_account.address, 10_000_000, currency_code="GBP",auth_key_prefix=swap_account.auth_key_prefix,is_blocking=True)

    client.swap_add_liquidity(liquidity_account, "USD", "EUR", 3243244, 4354435)
    client.swap_add_liquidity(liquidity_account, "GBP", "EUR", 4534452, 2443244)
    out, _ = client.swap_get_swap_input_amount("GBP", "USD", 243444)
    bb = client.get_balance(swap_account.address, "USD")
    client.swap(swap_account, "GBP", "USD", out)
    ab = client.get_balance(swap_account.address, "USD")
    assert 243444-1 <= ab - bb <= 243444+1

def test_swap_get_liquidity_output_amount():
    wallet = Wallet.new()

    liquidity_account = wallet.new_account()
    client.mint_coin(liquidity_account.address, 10_000_000, auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True, currency_code="USD")
    client.add_currency_to_account(liquidity_account, "EUR")
    client.mint_coin(liquidity_account.address, 10_000_000, currency_code="EUR",auth_key_prefix=liquidity_account.auth_key_prefix,is_blocking=True)
    client.add_currency_to_account(liquidity_account, "GBP")
    client.mint_coin(liquidity_account.address, 10_000_000, currency_code="GBP",auth_key_prefix=liquidity_account.auth_key_prefix,is_blocking=True)

    swap_account = wallet.new_account()
    client.mint_coin(swap_account.address, 10_000_000, auth_key_prefix=swap_account.auth_key_prefix,is_blocking=True, currency_code="USD")
    client.add_currency_to_account(swap_account, "EUR")
    client.mint_coin(swap_account.address, 10_000_000, currency_code="EUR",auth_key_prefix=swap_account.auth_key_prefix,is_blocking=True)
    client.add_currency_to_account(swap_account, "GBP")
    client.mint_coin(swap_account.address, 10_000_000, currency_code="GBP",auth_key_prefix=swap_account.auth_key_prefix,is_blocking=True)

    client.swap_add_liquidity(liquidity_account, "USD", "EUR", 3243243, 432432)
    out = client.swap_get_liquidity_output_amount("EUR", "USD", 243244)
    bc1b = client.get_balance(liquidity_account.address, "EUR")
    client.swap_add_liquidity(liquidity_account, "USD", "EUR", out, 1000000000)
    ac1b = client.get_balance(liquidity_account.address, "EUR")
    assert bc1b - ac1b == 243244


def test_get_currency_max_output_path():
    wallet = Wallet.new()

    liquidity_account = wallet.new_account()
    client.mint_coin(liquidity_account.address, 10_000_000, auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True, currency_code="USD")
    client.add_currency_to_account(liquidity_account, "EUR")
    client.mint_coin(liquidity_account.address, 10_000_000, currency_code="EUR", auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True)
    client.add_currency_to_account(liquidity_account, "GBP")
    client.mint_coin(liquidity_account.address, 10_000_000, currency_code="GBP", auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True)

    swap_account = wallet.new_account()
    client.mint_coin(swap_account.address, 10_000_000, auth_key_prefix=swap_account.auth_key_prefix, is_blocking=True, currency_code="USD")
    client.add_currency_to_account(swap_account, "EUR")
    client.mint_coin(swap_account.address, 10_000_000, currency_code="EUR", auth_key_prefix=swap_account.auth_key_prefix, is_blocking=True)
    client.add_currency_to_account(swap_account, "GBP")
    client.mint_coin(swap_account.address, 10_000_000, currency_code="GBP", auth_key_prefix=swap_account.auth_key_prefix, is_blocking=True)

    client.swap_add_liquidity(liquidity_account, "USD", "EUR", 250_000, 100_000)
    client.swap_add_liquidity(liquidity_account, "GBP", "EUR", 200_000, 100_000)
    client.swap_add_liquidity(liquidity_account, "GBP", "USD", 100_000, 100_000)
    path = client.get_currency_max_output_path("GBP", "USD", 20000)
    assert path == client.swap_get_currency_indexs("GBP", "EUR", "USD")

def test_get_currency_min_input_path():
    wallet = Wallet.new()

    liquidity_account = wallet.new_account()
    client.mint_coin(liquidity_account.address, 10_000_000, auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True, currency_code="USD")
    client.add_currency_to_account(liquidity_account, "EUR")
    client.mint_coin(liquidity_account.address, 10_000_000, currency_code="EUR", auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True)
    client.add_currency_to_account(liquidity_account, "GBP")
    client.mint_coin(liquidity_account.address, 10_000_000, currency_code="GBP", auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True)

    swap_account = wallet.new_account()
    client.mint_coin(swap_account.address, 10_000_000, auth_key_prefix=swap_account.auth_key_prefix, is_blocking=True, currency_code="USD")
    client.add_currency_to_account(swap_account, "EUR")
    client.mint_coin(swap_account.address, 10_000_000, currency_code="EUR", auth_key_prefix=swap_account.auth_key_prefix, is_blocking=True)
    client.add_currency_to_account(swap_account, "GBP")
    client.mint_coin(swap_account.address, 10_000_000, currency_code="GBP", auth_key_prefix=swap_account.auth_key_prefix, is_blocking=True)

    client.swap_add_liquidity(liquidity_account, "USD", "EUR", 250_000, 100_000)
    client.swap_add_liquidity(liquidity_account, "GBP", "EUR", 200_000, 100_000)
    client.swap_add_liquidity(liquidity_account, "GBP", "USD", 100_000, 100_000)
    path = client.get_currency_min_input_path("GBP", "USD", 20000)
    assert path == client.swap_get_currency_indexs("GBP", "EUR", "USD")
