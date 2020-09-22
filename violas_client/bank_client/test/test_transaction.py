from violas_client import Client, Wallet
from violas_client.banktypes.bytecode import CodeType
from violas_client.lbrtypes.bytecode import CodeType as LibraCodeType
from violas_client.move_core_types.language_storage import core_code_address



client = Client()
module_address = "da13aace1aa1c49e497416a9dd062ecb"
client.set_bank_module_address(core_code_address())
client.set_bank_owner_address(module_address)

def test_get_code_type():
    wallet = Wallet.new()
    module_account = wallet.new_account()
    client.mint_coin(module_account.address, 200_000_000, auth_key_prefix=module_account.auth_key_prefix, currency_code="USD")
    seq = client.bank_publish(module_account)
    assert client.get_account_transaction(module_account.address, seq).get_code_type() == CodeType.PUBLISH

    a1 = wallet.new_account()
    client.mint_coin(a1.address, 300_000_000, auth_key_prefix=a1.auth_key_prefix, currency_code="USD")
    seq = client.bank_publish(a1)
    assert client.get_account_transaction(a1.address, seq).get_code_type() == CodeType.PUBLISH

    seq = client.bank_lock(a1, 100_000_000, currency_code="USD")
    assert client.get_account_transaction(a1.address, seq).get_code_type() == CodeType.LOCK2

    seq = client.bank_borrow(a1, 1_000, currency_code="USD")
    assert client.get_account_transaction(a1.address, seq).get_code_type() == CodeType.BORROW2
    _, amount = client.bank_get_borrow_amount(a1.address, currency_code="USD")
    seq = client.bank_repay_borrow(a1, currency_code="USD", amount=amount)
    assert client.get_account_transaction(a1.address, seq).get_code_type() == CodeType.REPAY_BORROW2
    amount = client.bank_get_lock_amount(a1.address, currency_code="USD")
    seq = client.bank_redeem(a1, currency_code="USD", amount=amount)
    assert client.get_account_transaction(a1.address, seq).get_code_type() == CodeType.REDEEM2

def test_get_amount():
    wallet = Wallet.new()
    module_account = wallet.new_account()
    client.mint_coin(module_account.address, 200_000_000, auth_key_prefix=module_account.auth_key_prefix, currency_code="USD")
    seq = client.bank_publish(module_account)
    assert client.get_account_transaction(module_account.address, seq).get_amount() == None

    a1 = wallet.new_account()
    client.mint_coin(a1.address, 300_000_000, auth_key_prefix=a1.auth_key_prefix, currency_code="USD")
    seq = client.bank_publish(a1)
    assert client.get_account_transaction(a1.address, seq).get_amount() == None

    seq = client.bank_lock(a1, 100_000_000, currency_code="USD")
    assert client.get_account_transaction(a1.address, seq).get_amount() == 100_000_000

    seq = client.bank_borrow(a1, 1_000, currency_code="USD")
    assert client.get_account_transaction(a1.address, seq).get_amount() == 1_000

    seq = client.bank_repay_borrow(a1, amount=100, currency_code="USD")
    assert client.get_account_transaction(a1.address, seq).get_amount() == 100

    seq = client.bank_redeem(a1, currency_code="USD", amount=100)
    assert client.get_account_transaction(a1.address, seq).get_amount() == 100

def test_get_currency_code():
    wallet = Wallet.new()
    module_account = wallet.new_account()
    client = Client()
    client.mint_coin(module_account.address, 200_000_000, auth_key_prefix=module_account.auth_key_prefix, currency_code="USD")
    seq = client.bank_publish(module_account)
    assert client.get_account_transaction(module_account.address, seq).get_currency_code() == None

    a1 = wallet.new_account()
    client.mint_coin(a1.address, 300_000_000, auth_key_prefix=a1.auth_key_prefix, currency_code="USD")
    seq = client.bank_publish(a1)
    assert client.get_account_transaction(a1.address, seq).get_currency_code() == None

    seq = client.bank_lock(a1, 100_000_000, currency_code="USD")
    assert client.get_account_transaction(a1.address, seq).get_currency_code() == "USD"

    seq = client.bank_borrow(a1, 1_000, currency_code="USD")
    assert client.get_account_transaction(a1.address, seq).get_currency_code() == "USD"

    seq = client.bank_repay_borrow(a1, amount=100, currency_code="USD")
    assert client.get_account_transaction(a1.address, seq).get_currency_code() == "USD"

    seq = client.bank_redeem(a1, amount=100, currency_code="USD")
    assert client.get_account_transaction(a1.address, seq).get_currency_code() == "USD"

def test_get_data():
    data = "data"
    data_hex = b"data".hex()
    wallet = Wallet.new()
    module_account = wallet.new_account()
    client.mint_coin(module_account.address, 200_000_000, auth_key_prefix=module_account.auth_key_prefix, currency_code="USD")
    seq = client.bank_publish(module_account, data=data)
    assert client.get_account_transaction(module_account.address, seq).get_data() == data_hex

    a1 = wallet.new_account()
    client.mint_coin(a1.address, 300_000_000, auth_key_prefix=a1.auth_key_prefix, currency_code="USD")
    seq = client.bank_publish(a1, data=data)
    assert client.get_account_transaction(a1.address, seq).get_data() == data_hex

    seq = client.bank_lock(a1, 100_000_000, currency_code="USD", data=data)
    assert client.get_account_transaction(a1.address, seq).get_data() == data_hex

    seq = client.bank_borrow(a1, 1_000, currency_code="USD", data=data)
    assert client.get_account_transaction(a1.address, seq).get_data() == data_hex

    seq = client.bank_repay_borrow(a1, amount=100, currency_code="USD", data=data)
    assert client.get_account_transaction(a1.address, seq).get_data() == data_hex

    seq = client.bank_redeem(a1, amount=100, currency_code="USD", data=data)
    assert client.get_account_transaction(a1.address, seq).get_data() == data_hex
