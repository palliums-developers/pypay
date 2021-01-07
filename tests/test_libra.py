# libra test

from libra_client import Wallet, Client

def test_libra:
    #wallet = Wallet.new()
    wallet = Wallet.new_from_mnemonic("exercise kitchen spawn catalog hair intact shrimp stem version flee ozone exhibit")
    mnemonic = wallet.mnemonic
    print("mnemonic: ", mnemonic)

    account = wallet.new_account()
    address = wallet.accounts[0].address_hex
    print("address: ", address)

    client = Client("libra_testnet")
    balance = client.get_balance(account.address, "LBR")
    print("balance: ", balance)

    client.mint_coin(account.address, 10_000_000, auth_key_prefix=account.auth_key_prefix, is_blocking=True)
    balance = client.get_balance(account.address, "LBR")
    print("balance: ", balance)
