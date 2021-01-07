from bit import PrivateKeyTestnet
import struct, array
from ctypes import create_string_buffer


def test_create_ex_start(toaddress, sequence, module, outamount, times):
    try:
        btoaddress = bytes.fromhex(toaddress)
        bmodule = bytes.fromhex(module)
        datas = create_string_buffer(len(btoaddress) + 8 + len(bmodule) + 8 + 2)

        data_offer = 0
        struct.pack_into(f">{len(btoaddress)}sQ{len(bmodule)}sQH", datas, data_offer, 
                btoaddress, 
                sequence, 
                bmodule, 
                outamount, 
                times)
    except Exception as e:
        print(e)

    return datas

def test_create_ex_end(toaddress, sequence, amount, version):
    try:
        btoaddress = bytes.fromhex(toaddress)
        datas = create_string_buffer(len(btoaddress) + 8 + 8 + 8)

        data_offer = 0
        struct.pack_into(f">{len(btoaddress)}sQQQ", datas, data_offer, btoaddress, sequence, amount, version)

    except Exception as e:
        print(e)
    return datas

def test_create_ex_cancel(toaddress, sequence):
    try:
        btoaddress = bytes.fromhex(toaddress)
        datas = create_string_buffer(len(btoaddress) + 8)

        data_offer = 0
        struct.pack_into(f">{len(btoaddress)}sQ", datas, data_offer, btoaddress, sequence)

    except Exception as e:
        print(e)
    return datas

def test_create_ex_stop(toaddress, sequence):
    try:
        btoaddress = bytes.fromhex(toaddress)
        datas = create_string_buffer(len(btoaddress) + 8)

        data_offer = 0
        struct.pack_into(f">{len(btoaddress)}sQ", datas, data_offer, btoaddress, sequence)

    except Exception as e:
        print(e)
    return datas

def test_create_ex_mark(toaddress, sequence, version, amount):
    try:
        btoaddress = bytes.fromhex(toaddress)
        datas = create_string_buffer(len(btoaddress) + 8 + 8 + 8)

        data_offer = 0
        struct.pack_into(f">{len(btoaddress)}sQQQ", datas, data_offer, btoaddress, sequence, version, amount)

    except Exception as e:
        print(e)
    return datas

def test_create_btc_mark(toaddress, sequence, amount, name):
    try:
        btoaddress = bytes.fromhex(toaddress)
        bname = str.encode(name)
        datas = create_string_buffer(len(btoaddress) + 8 + 8 + len(bname))

        data_offer = 0
        print(bname)
        struct.pack_into(f">{len(btoaddress)}sQQ{len(bname)}s", datas, data_offer, btoaddress, sequence, amount, bname)

    except Exception as e:
        print(e)
    return datas

toaddress = "c91806cabcd5b2b5fa25ae1c50bed3c6"
sequence = 20200511
module = "e1be1ab8360a35a0259f1c93e3eac736"
outamount = 100000
times = 123
print(f'''************************************************************************create ex start
toaddress:{toaddress}
sequence: {sequence}
module:{module}
outammount:{outamount}
times:{times}
**********************************************************************************''')
datas = create_ex_start(toaddress, sequence, module, outamount, times)
print(datas)

my_key = PrivateKeyTestnet('cPRasph9hqhpPexNMTSeuAoqAiXgsN8R7fsFjFPzCSwWvZNsfEKj')
#print("wif: ", my_key.to_wif())
#print("address: ", my_key.address)  # mqCdj3UGbFaMQz3Mqk5wR5M9BmWUSkEQVr
#print("balance: ", my_key.get_balance('btc'))
#print("unspents: ", my_key.get_unspents())
#print("transactions: ", my_key.get_transactions())

print(my_key.create_transaction([('mqCdj3UGbFaMQz3Mqk5wR5M9BmWUSkEQVr', 0.00001000, 'btc')], message=datas, message_is_hex=True))


<ctypes.c_char_Array_50 object at 0x7f0b2a8e57c0>
0100000007b76d98a4871927cf457292e6a631c056d8b18bc31d5f0b06c93050d118059efb000000006b483045022100fda71e70fc787cef481306fb47ae1e06b1ccfb8a3e80a9dc319d45628bb7f1d502201562ca3f19f1c9199fe1ecf5559e54710dc9b42f64ee12f88346ae60084a1dfa012103e807dbecf9373cc3c2d6f2d2a7e38d524c1403840316299179782f0e97121018ffffffffdc88ccd6691e0c9d0c757c2a41da13cc5b9e2fe591e3d69ab31e9cc89582381b000000006a47304402206de7853eb23ab0cad579ca8911308a4d69f3d08804562a69bad813f75f3ff4e8022076791dbaff03dee5039699fe8627f88abca97b3626d33595b2274fefc605935c012103e807dbecf9373cc3c2d6f2d2a7e38d524c1403840316299179782f0e97121018ffffffff410402e9ca39b5a4211f297bf163882046d8d5a3fd4353d5692d3d5eb44fef84010000006a473044022063c7d09f26472b096b9e927095a946aa6a708995fbb1d54081b37547408fb83502201aba4e05f9122e1a321e02ed441c486cb264badb7a3633b1f84f12d450bb2948012103e807dbecf9373cc3c2d6f2d2a7e38d524c1403840316299179782f0e97121018ffffffff91bc24daca816ec303d8bcd9c1ea38e6042cbe9a05b3f1354fad2766fa7ce21b000000006b483045022100d70f4965556900b3dc7d37069379b8ce19cbb68ee860b6628ace46692251894e022051d8788611b85dcd5fe457ddf72fe3aff54193b8afffafb4c1ffeec3c61cd7af012103e807dbecf9373cc3c2d6f2d2a7e38d524c1403840316299179782f0e97121018ffffffffa7f75f3bee16e7dcd9614ab387910bc7766d36c2d27e7212a1be5a4e406b4f98000000006b483045022100866c2b111ef5ea7a8a47c756004f38067f245b953545688405ed6feb006f051c02200dbcee4b8138b6cd72d7b29d621e2db1dd2633327d805ddaf43d8af0638f862c012103e807dbecf9373cc3c2d6f2d2a7e38d524c1403840316299179782f0e97121018ffffffff44845aa84f5db114bb99264d7800c26e10aec0f1df11af61f019c9296f8074ad000000006b483045022100c4111ae7c6fc26c043c2838bd91651aed0adee8af53a14fbeb496047c9789751022060ddc21ddd7d1e24f2526ee77ff9fb407f3c27b2ba7b9806f2629af1dc240113012103e807dbecf9373cc3c2d6f2d2a7e38d524c1403840316299179782f0e97121018ffffffff6817788b0feb1b1524377f4cd206a5c1130b130dc94b1ee1d41349bf61f62c67000000006b483045022100faf6aa8f62795fd37021a9c078bc3ab754eeb587960c077e46b0b96fca96eee7022028d538eef5d45213b0d3a0b913bdc09567d3667c25e39b19757e76df0ef3b127012103e807dbecf9373cc3c2d6f2d2a7e38d524c1403840316299179782f0e97121018ffffffff03e8030000000000001976a9146a3a45105db9015dfe2db3ab222cf67661b2f68888ac38a50d00000000001976a9146a3a45105db9015dfe2db3ab222cf67661b2f68888ac0000000000000000346a32c91806cabcd5b2b5fa25ae1c50bed3c60000000001343c3fe1be1ab8360a35a0259f1c93e3eac73600000000000186a0007b00000000
