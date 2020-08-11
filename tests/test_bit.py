from bit import PrivateKeyTestnet

my_key = PrivateKeyTestnet('cPRasph9hqhpPexNMTSeuAoqAiXgsN8R7fsFjFPzCSwWvZNsfEKj')
#print("wif: ", my_key.to_wif())
#print("address: ", my_key.address)  # mqCdj3UGbFaMQz3Mqk5wR5M9BmWUSkEQVr
#print("balance: ", my_key.get_balance('btc'))
#print("unspents: ", my_key.get_unspents())
#print("transactions: ", my_key.get_transactions())

print(my_key.create_transaction([('mqCdj3UGbFaMQz3Mqk5wR5M9BmWUSkEQVr', 0.00001000, 'btc')]))
