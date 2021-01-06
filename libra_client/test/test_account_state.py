from libra_client import Client, Wallet

def test_exist():
    client = Client()
    wallet = Wallet.new()
    a1 = wallet.new_account()
    ac = client.get_account_state(a1.address)
    assert None == ac
    client.mint_coin(a1.address, 100, auth_key_prefix=a1.auth_key_prefix)
    ac = client.get_account_state(a1.address)
    assert None != ac

def test_get_sequence_number():
    client = Client()
    wallet = Wallet.new()
    a1 = wallet.new_account()
    a2 = wallet.new_account()
    client.mint_coin(a1.address, 100, auth_key_prefix=a1.auth_key_prefix)
    client.mint_coin(a2.address, 100, auth_key_prefix=a2.auth_key_prefix)
    ac = client.get_account_state(a1.address)
    assert 0 == ac.get_sequence_number()
    client.transfer_coin(a1, a2.address, 10)
    ac = client.get_account_state(a1.address)
    assert 1 == ac.get_sequence_number()

def test_get_account_address():
    client = Client()
    wallet = Wallet.new()
    a1 = wallet.new_account()
    client.mint_coin(a1.address, 100, auth_key_prefix=a1.auth_key_prefix)
    ac = client.get_account_state(a1.address)
    assert ac.get_account_address() == a1.address_hex

def test_is_published():
    client = Client()
    wallet = Wallet.new()
    a1 = wallet.new_account()
    client.mint_coin(a1.address, 100, auth_key_prefix=a1.auth_key_prefix)
    ac = client.get_account_state(a1.address)
    assert ac.is_published("XUS") == True
