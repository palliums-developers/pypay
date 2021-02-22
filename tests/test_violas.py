# violas test

from violas_client import Wallet, Client

def test_violas():
    ##wallet = Wallet.new()
    #wallet = Wallet.new_from_mnemonic("exercise kitchen spawn catalog hair intact shrimp stem version flee ozone exhibit")
    #mnemonic = wallet.mnemonic
    #print("mnemonic: ", mnemonic)
    #
    #account = wallet.new_account()
    #address = wallet.accounts[0].address_hex
    #print("address: ", address)
    #
    ##client = Client("violas_testnet")
    #client = Client("violas_testnet_out")
    #balance = client.get_balance(account.address, "LBR")
    #print("balance: ", balance)
    #
    #client.mint_coin(account.address, 10_000_000, auth_key_prefix=account.auth_key_prefix, is_blocking=True)
    #balance = client.get_balance(account.address, "LBR")
    #print("balance: ", balance)
    #
    #client.mint_coin(account.address, 10_000_000, auth_key_prefix=account.auth_key_prefix, is_blocking=True, currency_code="VLSUSD")
    #client.transfer_coin(account, '332c87f481f1180a34410d795d12cf9d', 100, currency_code='VLSUSD')



    # --------------------------------------
    # 钱包                                                                                            
    #wallet = Wallet.new_from_mnemonic('head invite face tomato away romance kite avoid edge hotel try debate')                                                                               
    #print("mnemonic: ", wallet.mnemonic)                                                                

    # 账户地址                                                                                          
    #account = wallet.new_account()                                                                      
    #print("account addr: ", account.address.hex())                                                      
    #account1 = wallet.new_account()                                                                     
    #print("account1 addr: ", account1.address.hex())                                                    

    # 账户余额                                                                                          
    #client = Client("violas_testnet_out")                                                                   
    #print("account balance: ", client.get_balance(account.address))                                     
    #print("account1 balance: ", client.get_balance(account1.address))                                   

    # 铸币                                                                                              
    #client.mint_coin(account.address, 10_000_000, auth_key_prefix=account.auth_key_prefix, currency_code="LBR")
    #client.mint_coin(account1.address, 10_000_000, auth_key_prefix=account1.auth_key_prefix, currency_code="LBR")
    #print("account balance: ", client.get_balance(account.address))                                     
    #print("account1 balance: ", client.get_balance(account1.address))                                   

    # 转账                                                                                              
    #client.mint_coin(account1.address, 1_000_000, auth_key_prefix=account.auth_key_prefix, currency_code="LBR")
    #client.transfer_coin(account, account1.address, 1_000_000)                                          
    #print("account balance: ", client.get_balance(account.address))                                     
    #print("account1 balance: ", client.get_balance(account1.address))                                   

    # 添加币种                                                                                          
    #client.add_currency_to_account(account, currency_code="Coin1")                                      
    #client.mint_coin(account.address_hex, 10_000_000, auth_key_prefix=account.auth_key_prefix, currency_code="Coin1")
    #balances = client.get_balances(account.address_hex)                                                 
    #print("Coin1: ", balances["Coin1"])                                                                 

    # 转账Coin1                                                                                         
    #client.add_currency_to_account(account1, currency_code="Coin1")                                     
    #client.mint_coin(account1.address_hex, 10_000_000, auth_key_prefix=account1.auth_key_prefix, currency_code="Coin1")
    #client.transfer_coin(account, account1.address, 1_000_000, currency_code="Coin1")                   
    #balances = client.get_balances(account.address_hex)                                                 
    #print("account Coin1: ", balances["Coin1"])                                                         
    #balances1 = client.get_balances(account1.address_hex)                                               
    #print("account1 Coin1: ", balances1["Coin1"])


    # -------------------------------------------------------
    #wallet = Wallet.new()
    wallet = Wallet.new_from_mnemonic('tobacco pass render slam margin annual essay evoke expand finger eager host')                                                                               
    mnemonic = wallet.mnemonic
    print(mnemonic)
    client = Client("violas_testnet_out")                                                                   

    account = wallet.new_account()                                                                      
    print("account addr: ", account.address.hex())                                                      

    client.mint_coin(account.address, 10_000_000, auth_key_prefix=account.auth_key_prefix, currency_code="LBR")

    #client.add_currency_to_account(account, currency_code="VLSUSD")
    client.mint_coin(account.address, 10_000_000, auth_key_prefix=account.auth_key_prefix, currency_code="VLSUSD")

    #client.transfer_coin(account, 'e2edbffdec21a9873e79baebd80dc47f', 1_000_000, currency_code="VLSUSD")

    balances = client.get_balances(account.address_hex)
    print(balances)


if __name__ == '__main__':
    #wallet = Wallet.new()
    wallet = Wallet.new_from_mnemonic("drink unaware online call danger physical stadium choose report know clean fatigue")
    mnemonic = wallet.mnemonic
    print("mnemonic: ", mnemonic)
    
    account = wallet.new_account()
    address = wallet.accounts[0].address_hex
    print("address: ", address)
    prefix = wallet.accounts[0].auth_key_prefix.hex()
    print("prefix: ", prefix)
    
    client = Client("violas_testnet")
    balance = client.get_balance(account.address, "VLS")
    print("balance: ", balance)
    
    client.transfer_coin(account, "8e1a89070ff3f632e69b3e431625ccff", 10_000)                                          
