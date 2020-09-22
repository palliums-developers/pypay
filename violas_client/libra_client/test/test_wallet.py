from violas_client.libra_client.wallet_library import Wallet

def test_recover():
    file_name = "./recover"
    wallet = Wallet.new()
    a1 = wallet.new_account()
    wallet.write_recovery(file_name)
    wallet = Wallet.recover(file_name)
    assert a1.address == wallet.accounts[0].address
    a2 = wallet.get_account_by_address_or_refid(a1.address)
    a3 = wallet.get_account_by_address_or_refid(0)
    assert a2.address == a1.address
    assert a3.address == a1.address
