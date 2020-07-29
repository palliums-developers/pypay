from enum import IntEnum
from violas_client.move_core_types.account_address import AccountAddress
from violas_client.lbrtypes.bytecode import gen_hex_hash
from violas_client.lbrtypes.bytecode import CodeType as LibraCodeType

class CodeType(IntEnum):
    EXCHANGE = 1000
    EXDEP = 1001
    ADD_CURRENCY = 1002
    ADD_LIQUIDITY = 1003
    INITIALIZE = 1004
    REMOVE_LIQUIDITY = 1005
    SWAP = 1006

bytecodes = {
    "exchange": b'\xa1\x1c\xeb\x0b\x01\x00\x0b\x01\x00\x10\x02\x10(\x038\xdf\x01\x04\x97\x02R\x05\xe9\x02\x98\x03\x07\x81\x06\x8b\x05\x08\x8c\x0b \x06\xac\x0b\x16\n\xc2\x0b-\x0c\xef\x0b\xde\x0e\r\xcd\x1a\x12\x00\x00\x01\x01\x00\x02\x01\x03\x01\x04\x01\x05\x01\x06\x01\x07\x00\x08\x01\x00\x00\t\x01\x00\x00\n\x01\x00\x00\x0b\x01\x00\x00\x0c\x01\x00\x00\r\x01\x00\x02\x18\x02\x00\x02\x19\x02\x00\x02\x1a\x02\x00\x02\r\x01\x00\x04\x0e\x00\x01\x01\x01\x07\x0f\x02\x03\x01\x01\x07\x10\x04\x05\x01\x01\x07\x11\x00\x06\x01\x01\x07\x12\x07\x08\x01\x01\x07\x13\t\n\x01\x01\x07\x14\x0b\x00\x01\x01\x06\x15\x0c\r\x00\x05\x16\r\x0e\x01\x01\x03\x17\x03\x01\x01\x01\x02\x1b\x0c\x00\x01\x01\x02\x1c\x00\n\x01\x01\x02\x1d\x0f\x10\x00\x02\x1e\x0f\x11\x00\x02\x1f\x12\x13\x00\x02 \x14\x00\x01\x01\x02!\x0c\x15\x00\x02"\x16\n\x00\x02#\x17\x16\x00\x02$\x18\x00\x01\x01\x01%\x03\x00\x01\x01\x00\x16\x00\x0e\x01\x01\x00\x1b\x0c\x00\x01\x01\x00&\x19\x00\x02\x01\x01\x00 \x1a\x00\x01\x01\x00\'\x00\n\x01\x01\x00(\x00\x1b\x00\x00)\r\n\x02\x01\x01\x00*\x00\x1c\x02\x01\x01\x00+\x00\x16\x02\x01\x01\x00,\x1d\x1e\x00\x00-\x1f \x00\x00.\x0c\x00\x00\x00/!\x16\x02\x01\x01\x000"\x00\x02\x01\x01\x001\x00\r\x00\x002#\x00\x02\x01\x01\x00$$\x00\x01\x01\x19%\x08%\x00%\x06\x01\n%\x15%\x15(\x1c)!)\x0f%\x04\x01\x19(\x0b%\x0b(\x051\x021\x061\x053\x023\x063\x031\x03\x01\x033\x00(\t\x11\x14\x11\x18%\x18(\t\x10\x14\x10%%%(\x057\x017\x03\n\x06\n\x01\n\x141\t\x13\x14\x13\x13%\x00\x01\n\x02\x02\x06\n\t\x00\x03\x01\x06\t\x00\x02\x07\n\t\x00\x03\x01\x07\t\x00\x01\n\t\x00\x02\x06\n\t\x00\x06\t\x00\x02\x01\x03\x01\x06\n\t\x00\x01\x03\x02\x07\n\t\x00\t\x00\x01\x06\x0c\x01\x05\x01\x01\x05\n\x02\x03\n\x02\x03\x03\x01\x08\x06\x01\x08\x07\x05\n\x02\x03\n\x02\x03\n\x02\x01\x08\x08\x04\x06\x0c\x06\x08\t\x03\n\x02\x01\x08\t\x03\x03\x03\x03\x07\x03\x03\x03\x03\x03\x03\x03\x05\x06\x0c\x05\x06\x08\t\x03\n\x02\x05\x06\x0c\x03\x03\x03\x03\x03\x06\x0c\x03\n\x02\x01\n\n\x02\x02\x03\x03\x03\x03\x03\x07\x08\x02\x01\x07\x08\x01\x02\x03\x07\x08\x04\x01\x07\x08\x03\n\x06\x0c\x03\x03\x03\x03\x03\x03\x03\x03\x03\x04\x06\x0c\x03\x03\x03\x06\x06\x0c\x05\x03\x03\n\x02\n\x02\x04\x06\x0c\x05\x03\n\x02\x01\t\x00\x02\n\x02\x07\x08\x00\r\x03\x03\x03\x03\x07\x08\x01\x03\x03\x07\x08\x02\x01\x03\x01\x03\x03\x01\t\x01\x02\t\x00\t\x01\x01\x06\x08\x05\x06\n\x02\n\n\x02\x01\x03\x01\x03\x01\x07\x08\x00\x07\x03\x03\x03\x01\x03\x07\x08\x03\x07\x08\x04\x04\x03\x03\x01\x03\t\x03\x03\x07\x08\x01\x07\x08\x02\x01\x03\x01\x03\x03\x08\x03\x03\x07\x08\x01\x07\x08\x01\x07\n\x08\x01\x01\x03\x01\x01\x08\x01\x05\x03\x03\x07\x08\x03\x07\x08\x03\x07\n\x08\x03\x01\x08\x03\x0b\x03\x03\n\x02\n\x02\x03\x03\n\x02\x08\x07\x05\x07\x08\x03\x07\x08\x04\x13\x03\x03\x08\x06\n\x02\n\x02\x03\x03\x03\n\x02\x07\x08\x01\x03\x03\x07\x08\x02\x01\x03\x01\x07\x08\x03\x07\x08\x04\x03\x1d\x03\n\x03\x03\n\x02\n\x02\x03\x03\x03\x03\x03\x03\n\x02\x02\x02\x07\x08\x01\x07\x08\x01\x03\x03\x03\x03\x07\x08\x02\x08\x08\x01\x03\x01\x01\x01\x01\x03\x01\x02\x08Exchange\x05Debug\x05ExDep\x03LCS\x05Libra\x0cLibraAccount\x06Signer\x06Vector\x14RegisteredCurrencies\x07Reserve\x08Reserves\x05Token\x06Tokens\x12WithdrawCapability\rcurrency_code\x06borrow\nborrow_mut\x05empty\x08index_of\x06length\tpush_back\naddress_of\x10accepts_currency\x08to_bytes\tBurnEvent\tMintEvent\tSwapEvent\x0cadd_currency\x07balance\tc_b_event\tc_m_event\tc_s_event\x07deposit\x1bextract_withdraw_capability\x0eget_amount_out\x12get_mint_liquidity\x08withdraw\x05print\radd_liquidity\x0bget_coin_id\rget_currencys\x15get_liquidity_balance\x0fget_pair_indexs\x0bget_reserve\x14get_reserve_internal\tget_token\ninitialize\x04mint\x10remove_liquidity\x0esingleton_addr\x04swap\x0ecurrency_codes\x16liquidity_total_supply\x05coina\x05coinb\x08reserves\x05index\x05value\x06tokens\x03caprW\xc2A~M\x108\xe1\x81|\x8f(:\xce.\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\n\x02\x01\x00\x05\x10rW\xc2A~M\x108\xe1\x81|\x8f(:\xce.\x00\x02\x013\n\n\x02\x01\x02\x034\x035\x08\x036\x08\x03\x02\x02\x017\n\x08\x01\x03\x02\x028\x039\x03\x04\x02\x01:\n\x08\x03\x05\x02\x01;\x08\t\x15\x00\x01\x00\x00\x058\x00\x01\x11#8\x01\x02\x16\x01\x01\x00&\x0c8\x02\x0c\x01\x11#*\x00\x0c\x02\x0b\x02\x0f\x00\x0b\x018\x03\x0b\x008\x04\x02\x17\x01\x04\x00\x02\x04\x05\'K8\x05\x03\x03\x05\x068\x06\x0c\x0f\x05\x08\t\x0c\x0f\x0b\x0f\x0c\r\x0b\r\x03\r\x05G\x11#*\x02\x0c\x0c8\x07\x0c\x08\x0c\x07\n\x07\n\x08\x0b\x0c\x11\x1e\x0c\t\n\t\x10\x01\x14\n\t\x10\x02\x10\x03\x14\n\t\x10\x04\x10\x03\x14\x0c\x0b\x0c\n\x0c\x10\x0b\x00\n\x07\n\x08\n\x01\n\x02\n\x03\n\x04\n\n\n\x0b\n\x108\x08\x0c\x06\x0c\x05\x0c\x11\n\x11\n\t\x0f\x01\x15\n\n\n\x05\x16\n\t\x0f\x02\x0f\x03\x15\n\x0b\n\x06\x16\x0b\t\x0f\x04\x0f\x03\x15\x02\x0b\x00\x01\x06\xc4\x13\x00\x00\x00\x00\x00\x00\'\x18\x00\x01\x05*\n\x11#+\x05\x0c\x03\x0b\x00\x0b\x03\x10\x05\n\x01\x0b\x028\t\x02\x19\x01\x01\x00+\x128\x02\x0c\x00\x11\x1a\x0c\x01\x0e\x01\x0e\x008\n\x0c\x03\x0c\x02\n\x02\x0c\x04\x0b\x04\x03\x0e\x05\x10\n\x03\x02\x06\x92\x13\x00\x00\x00\x00\x00\x00\'\x1a\x01\x01\x00,\x07\x11#*\x00\x0c\x00\x0b\x00\x10\x00\x14\x02\x1b\x01\x02\x00\x04-!8\x07\x0c\x03\x0c\x02\n\x021 /\n\x03\x16\x0c\x01\n\x00*\x04\x0c\x07\n\x01\x0b\x07\x11\x1f\x0c\x06\n\x06\x10\x03\x14\x06\x00\x00\x00\x00\x00\x00\x00\x00$\x0c\x04\x0b\x04\x03\x19\x05\x1d\x0b\x06\x10\x03\x14\x02\x0b\x06\x01\x06\x9c\x13\x00\x00\x00\x00\x00\x00\'\x1c\x01\x01\x00.\x108\x008\x0b\x0c\x01\x0c\x00\n\x00\n\x01#\x0c\x02\x0b\x02\x03\x0b\x05\x0e\n\x00\n\x01\x02\x06\xa6\x13\x00\x00\x00\x00\x00\x00\'\x1d\x01\x02\x00\x02/08\x07\x0c\x01\x0c\x00\x11#*\x02\x0c\x03\n\x00\n\x01\x0b\x03\x11\x1e\x0c\x028\x0c\x0c\x078\r\x0c\x08\n\x07\n\x02\x10\x02\x10\x03\x14!\x03\x17\x05\x1f\n\x08\n\x02\x10\x04\x10\x03\x14!\x0c\x06\x05!\t\x0c\x06\x0b\x06\x0c\x04\x0b\x04\x03&\x05,\x0b\x02\x10\x01\x14\n\x07\n\x08\x02\x0b\x02\x01\x06\xb0\x13\x00\x00\x00\x00\x00\x00\'\x1e\x00\x000N\n\x00\n\x01#\x0c\x08\x0b\x08\x03\x07\x05\x11\x0b\x02\x0f\x06\x0c\x07\x06\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x03\n\x07.8\x0e\x0c\x04\x05\x15\x0b\x02\x01\x06\xba\x13\x00\x00\x00\x00\x00\x00\'\n\x03\n\x04#\x03\x1a\x05>\n\x07\n\x038\x0f\x0c\x05\n\x05\x10\x02\x10\x07\x14\n\x00!\x03&\x05.\n\x05\x10\x04\x10\x07\x14\n\x01!\x0c\n\x050\t\x0c\n\x0b\n\x033\x057\x0b\x07\x01\x0b\x05\x02\x0b\x05\x01\n\x03\x06\x01\x00\x00\x00\x00\x00\x00\x00\x16\x0c\x03\x05\x15\n\x07\x06\x00\x00\x00\x00\x00\x00\x00\x00\n\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x12\x03\n\x01\x06\x00\x00\x00\x00\x00\x00\x00\x00\x12\x03\x12\x018\x10\x0b\x07\n\x038\x0f\x0c\x06\x0b\x06\x02\x1f\x00\x002/\x0b\x01\x0f\x08\x0c\x06\x06\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x02\n\x06.8\x11\x0c\x03\n\x02\n\x03#\x03\x0e\x05$\n\x06\n\x028\x12\x0c\x04\n\x04\x10\x07\x14\n\x00!\x03\x19\x05\x1d\x0b\x06\x01\x0b\x04\x02\x0b\x04\x01\n\x02\x06\x01\x00\x00\x00\x00\x00\x00\x00\x16\x0c\x02\x05\t\n\x06\n\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x12\x038\x13\x0b\x06\n\x028\x12\x0c\x05\x0b\x05\x02 \x01\x00\x08\x1a\n\x00\x11\x07\x11#!\x0c\x01\x0b\x01\x03\x08\x05\x16\n\x008\x14\x12\x02A\x02\n\x008\x15\x12\x00A\x00\n\x00\x0b\x00\x11\x10\x12\x05A\x05\x02\x0b\x00\x01\x06\x88\x13\x00\x00\x00\x00\x00\x00\'!\x00\x02\x04\x054J\n\x00\x11\x07\x0c\x12\n\x12)\x04 \x03\x08\x05\x0c\n\x008\x16\x12\x04A\x04\n\x011 /\n\x02\x16\x0c\x0e\n\x12*\x04\x0c\x14\n\x0e\x0b\x14\x11\x1f\x0c\x13\n\x03\n\x04\n\x05\n\x06\n\x07\n\x08\n\t\x11\x12\x0c\x0b\x0c\n\x0c\x0f\n\x13\x10\x03\x14\n\x0f\x16\x0b\x13\x0f\x03\x158\x02\x0c\x0c8\x17\x0c\r\x0b\x0c\n\n\x0b\r\n\x0b\n\x0f\x11\r\x0c\x11\x0e\x118\x18\x0c\x10\x0e\x118\x19\n\x00\n\n\x0b\x108\x1a\x0b\x00\n\x0b\x07\x008\x1b\n\t\n\x0f\x16\n\n\n\x0b\x02"\x01\x04\x00\x02\x04\x055\x8d\x01\x11#*\x02\x0c\x108\x07\x0c\x0b\x0c\n\n\n\n\x0b\x0b\x10\x11\x1e\x0c\r\n\r\x10\x01\x14\n\r\x10\x02\x10\x03\x14\n\r\x10\x04\x10\x03\x14\x0c\x0f\x0c\x0e\x0c\x16\n\x00\x11\x07*\x04\x0c\x15\n\n1 /\n\x0b\x16\x0c\t\n\t\x0b\x15\x11\x1f\x0c\x14\n\x015\n\x0e5\x18\n\x165\x1a4\x0c\x04\n\x015\n\x0f5\x18\n\x165\x1a4\x0c\x05\n\x04\n\x02&\x03@\x05E\n\x05\n\x03&\x0c\x13\x05G\t\x0c\x13\x0b\x13\x0c\x11\x0b\x11\x03L\x05\x85\x01\n\x16\n\x01\x17\n\r\x0f\x01\x15\n\x0e\n\x04\x17\n\r\x0f\x02\x0f\x03\x15\n\x0f\n\x05\x17\x0b\r\x0f\x04\x0f\x03\x15\n\x14\x10\x03\x14\n\x01\x17\x0b\x14\x0f\x03\x158\x02\x0c\x078\x17\x0c\x08\x0b\x07\n\x04\x0b\x08\n\x05\n\x01\x11\x0c\x0c\x06\x0e\x068\x1c\x0c\x0c\x0e\x068\x1d\n\x00\n\x00\x11\x07\n\x04\x0b\x0c8\x1e\n\x00\x0b\x00\x11\x07\n\x05\x07\x008\x1f\x02\x0b\x14\x01\x0b\r\x01\x0b\x00\x01\x06\xce\x13\x00\x00\x00\x00\x00\x00\'#\x00\x00\x00\x02\x07\x01\x02$\x01\x03\x00\x02\x056\x8a\x028\x07\x0c\x0f\x0c\x0e\x0e\x048 \x0c\x10\x0e\x04\x06\x00\x00\x00\x00\x00\x00\x00\x008!\x14\x0e\x04\n\x10\x06\x01\x00\x00\x00\x00\x00\x00\x00\x178!\x14\x0c\x13\x0c\x12\n\x12\n\x13$\x03\x17\x05\x1b\n\x0f\n\x0e\x0c\x0f\x0c\x0e\n\x10\x06\x01\x00\x00\x00\x00\x00\x00\x00$\x03 \x05%\n\x0e\n\x0f"\x0c\x1e\x05\'\t\x0c\x1e\x0b\x1e\x03*\x050\n\x0e\n\x124!\x0c\x1f\x052\t\x0c\x1f\x0b\x1f\x035\x05;\n\x0f\n\x134!\x0c \x05=\t\x0c \x0b \x0c\x1c\x0b\x1c\x03B\x05O8"\x0c\x07\r\x07\n\x028#\x11#*\x02\x0c\x1a\x06\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x0b\x06\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x06\x05S\x0b\x00\x01\x06\xd8\x13\x00\x00\x00\x00\x00\x00\'\n\x0b\n\x10\x06\x01\x00\x00\x00\x00\x00\x00\x00\x17#\x03Z\x05\xd4\x01\x0e\x07\n\x0b8$\x14\x0c\x08\x0e\x04\n\x0b8!\x144\x0c\x0c\x0e\x04\n\x0b\x06\x01\x00\x00\x00\x00\x00\x00\x00\x168!\x144\x0c\r\n\x0c\n\r#\x03r\x05\xa1\x01\n\x0c\n\r\n\x1a\x11\x1e\x0c\x14\n\x14\x10\x02\x10\x03\x14\n\x14\x10\x04\x10\x03\x14\x0c\x18\x0c\x16\n\x08\n\x16\n\x18\x11\x11\x0c\x06\r\x07\n\x068#\n\x14\x10\x02\x10\x03\x14\n\x08\x16\n\x14\x0f\x02\x0f\x03\x15\n\x14\x10\x04\x10\x03\x14\n\x06\x17\n\x14\x0f\x04\x0f\x03\x15\x0b\x14.8%\x05\xcf\x01\n\r\n\x0c\n\x1a\x11\x1e\x0c\x15\n\x15\x10\x04\x10\x03\x14\n\x15\x10\x02\x10\x03\x14\x0c\x19\x0c\x17\n\x08\n\x17\n\x19\x11\x11\x0c\x06\r\x07\n\x068#\n\x15\x10\x02\x10\x03\x14\n\x06\x17\n\x15\x0f\x02\x0f\x03\x15\n\x15\x10\x04\x10\x03\x14\n\x08\x16\n\x15\x0f\x04\x0f\x03\x15\x0b\x15.8%\n\x0b\x06\x01\x00\x00\x00\x00\x00\x00\x00\x16\x0c\x0b\x05S\x0b\x1a\x01\n\x06\n\x03&\x0c!\x0b!\x03\xdd\x01\x05\xf2\x018\x02\x0c\t8\x17\x0c\n\x0b\t\n\x02\x0b\n\n\x06\x0b\x05\x11\x0e\x0c\x1b\x0e\x1b8&\x0c\x11\x0e\x1b8\'\n\x12\n\x13#\x03\xf6\x01\x05\x80\x02\x0b\x00\x01\x06\xd9\x13\x00\x00\x00\x00\x00\x00\'\n\x00\n\x02\x0b\x118\x1a\x0b\x00\n\x01\n\x06\x07\x008\x1f\x05\x89\x02\n\x00\n\x02\x0b\x118\x1b\x0b\x00\n\x01\n\x06\x07\x008\x1e\x02%\x00\x01\x05*\x0b\x11#+\x05\x0c\x04\x0b\x00\n\x01\x0b\x04\x10\x05\n\x02\x0b\x038(\x02\x00\x00\x01\x00\x01\x01\x03\x01\x01\x02\x05\x00\x02\x00\x03\x00\x04\x00\x00',
    "exdep": b'\xa1\x1c\xeb\x0b\x01\x00\r\x01\x00\x08\x02\x08\x1e\x03&\x8f\x01\x04\xb5\x01\x12\x05\xc7\x01\xe6\x01\x07\xad\x03\x98\x04\x08\xc5\x07 \x06\xe5\x07\x16\n\xfb\x07=\x0b\xb8\x08\x02\x0c\xba\x08\xba\x08\r\xf4\x10\x04\x0e\xf8\x10\x02\x00\x00\x01\x01\x01\x02\x01\x03\x00\x04\x01\x01\x01\x00\x05\x02\x00\x00\x06\x02\x00\x00\x07\x02\x00\x00\x08\x01\x00\x01\x01\x01\x01\x01\x02\x08\x01\x00\x01\t\x00\x01\x01\x01\x01\n\x02\x03\x01\x01\x01\x0b\x04\x05\x01\x01\x01\x0c\x01\x05\x01\x01\x03\r\x06\x07\x00\x02\t\x08\x01\x01\x01\x02\x0e\t\x01\x01\x01\x02\x0f\x06\n\x00\x02\x10\x0b\x01\x01\x01\x02\x11\n\x01\x00\x02\x12\x0c\x05\x01\x01\x00\x13\x06\x01\x01\x01\x00\x14\x01\x03\x01\x01\x00\x15\r\x03\x01\x01\x00\x16\x0e\x0f\x00\x00\x17\x0e\x10\x00\x00\x18\x11\x12\x00\x00\t\x13\x01\x01\x01\x00\x0f\x06\x14\x00\x00\x19\x15\x03\x00\x00\x1a\x16\x15\x00\x00\x1b\x17\x03\x00\x00\x1c\x15\x03\x00\x00\x1d\x01\x07\x00\x00\x1e\x18\x03\x00\x00\x0b\x19\x01\x01\x01\x03\x1b\r\x1b\x01\x1b\n\x1b\x06\x1b\x00\x1b\x02\x1b\x05\x1b\x08\x1b\x02\x07\x0b\x05\x01\t\x00\x0b\x05\x01\t\x00\x00\x01\x06\x0b\x05\x01\t\x00\x01\x03\x02\x07\x0b\x05\x01\t\x00\x03\x01\x0b\x05\x01\t\x00\x01\x06\x0c\x01\x05\x03\x06\x0c\x05\x0b\x05\x01\t\x00\x05\x06\x0c\x05\x0b\x05\x01\t\x00\n\x02\n\x02\x01\x08\x06\x05\x06\x08\x06\x05\x03\n\x02\n\x02\x02\x06\x08\x06\x03\x01\x06\x0b\x00\x01\t\x00\x05\n\x02\x03\n\x02\x03\x03\x01\x08\x01\x01\x08\x02\x05\n\x02\x03\n\x02\x03\n\x02\x01\x08\x03\x04\x06\x0c\x06\x08\x04\x03\n\x02\x01\x08\x04\x03\x03\x03\x03\x07\x03\x03\x03\x03\x03\x03\x03\x02\x04\x04\x02\x03\x03\x05\x06\x0c\x05\x06\x08\x04\x03\n\x02\x02\x01\x03\x01\t\x00\x03\x07\x0b\x00\x01\t\x00\x08\x06\x0b\x05\x01\t\x00\x07\x04\x04\x04\x01\x03\x01\x01\x17\x03\x03\x03\x03\x04\x04\x04\x04\x04\x03\x01\x01\x03\x01\x03\x01\x03\x03\x03\x03\x03\x01\x03\x05\x03\x01\x03\x01\x01\x03\x04\x04\x04\x04\x07\x0b\x00\x01\t\x00\x0b\x05\x01\t\x00\x01\x03\x05ExDep\x05Libra\x0cLibraAccount\x06Signer\x07Balance\tBurnEvent\tMintEvent\tSwapEvent\x12WithdrawCapability\x07deposit\x05value\x08withdraw\x04zero\naddress_of\x15deposit_with_metadata\x1bextract_withdraw_capability\x16pay_from_with_metadata\x1brestore_withdraw_capability\rwithdraw_from\x0cadd_currency\x07balance\x0bbalance_for\tc_b_event\tc_m_event\tc_s_event\x0eget_amount_out\x12get_mint_liquidity\x03min\x05quote\x0esingleton_addr\x04sqrt\x04coin\x05coina\x10withdraw_amounta\x05coinb\x10withdraw_amountb\x0bburn_amount\x0fdeposit_amounta\x0fdeposit_amountb\x0bmint_amount\ninput_name\x0cinput_amount\x0boutput_name\routput_amount\x04data\x03caprW\xc2A~M\x108\xe1\x81|\x8f(:\xce.\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\n\x02\x01\x00\x05\x10rW\xc2A~M\x108\xe1\x81|\x8f(:\xce.\x00\x02\x01\x1f\x0b\x05\x01\t\x00\x01\x02\x05 \n\x02!\x03"\n\x02#\x03$\x03\x02\x02\x05 \n\x02%\x03"\n\x02&\x03\'\x03\x03\x02\x05(\n\x02)\x03*\n\x02+\x03,\n\x02\x04\x02\x01-\x08\x06\x00\x1b\x0b\x01\x00\x1a\x11\n\x00\x11\x04\x11\x17!\x0c\x01\x0b\x01\x03\x08\x05\r\x0b\x008\x009\x00B\x00\x02\x0b\x00\x01\x06\xaa\x0f\x00\x00\x00\x00\x00\x00\'\x0c\x01\x01\x00\x01\x04\x11\x17=\x008\x01\x02\r\x00\x00\x01\x04\x0b\x007\x008\x02\x02\x0e\x01\x00\x01\x07\x0b\x00\n\x01\x0b\x02\n\x03\n\x04\x12\x01\x02\x0f\x01\x00\x01\x07\x0b\x00\n\x01\x0b\x02\n\x03\n\x04\x12\x02\x02\x10\x01\x00\x01\x07\x0b\x00\n\x01\x0b\x02\n\x03\x0b\x04\x12\x03\x02\x11\x01\x01\x00\x1c\x1c\n\x00\x11\x07\x0c\x05\x0e\x05\n\x028\x03\x0c\x06\x0b\x05\x11\t\x0b\x00\x11\x17\x0b\x06\x0b\x03\x07\x008\x04\x0b\x01\x10\x01\n\x028\x03\x0c\x06\x11\x17<\x00\x0c\x04\x0b\x046\x00\x0b\x068\x05\x02\x12\x01\x00\x1a\x10\n\x00\x11\x04\x11\x17!\x0c\x01\x0b\x01\x03\x08\x05\x0c\x0b\x00\x11\x07\x12\x04\x02\x0b\x00\x01\x06\xa0\x0f\x00\x00\x00\x00\x00\x00\'\x13\x01\x00\x1d3\n\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00$\x03\x05\x05\n\n\x01\x06\x00\x00\x00\x00\x00\x00\x00\x00$\x0c\x08\x05\x0c\t\x0c\x08\x0b\x08\x03\x0f\x05\x14\n\x02\x06\x00\x00\x00\x00\x00\x00\x00\x00$\x0c\t\x05\x16\t\x0c\t\x0b\t\x0c\x06\x0b\x06\x03\x1b\x051\n\x0052\xe5\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\x0c\x03\n\x03\n\x025\x18\x0c\x05\n\x0152\xe8\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\n\x03\x16\x0c\x04\n\x05\n\x04\x1a4\x02\x06\xd2\x0f\x00\x00\x00\x00\x00\x00\'\x14\x01\x00\x1e\x85\x01\n\x04\x06\x00\x00\x00\x00\x00\x00\x00\x00!\x03\x05\x05\n\n\x05\x06\x00\x00\x00\x00\x00\x00\x00\x00!\x0c\x11\x05\x0c\t\x0c\x11\x0b\x11\x03\x0f\x05\x14\n\x00\n\x01\x0c\x1a\x0c\x19\x05M\n\x00\n\x04\n\x05\x11\x16\x0c\n\n\n\n\x01%\x03\x1e\x05,\n\n\n\x03&\x0c\x12\x0b\x12\x03%\x05*\n\x00\n\n\x0c\x18\x0c\x17\x05I\x06\xbe\x0f\x00\x00\x00\x00\x00\x00\'\n\x01\n\x05\n\x04\x11\x16\x0c\x08\n\x08\n\x00%\x036\x05;\n\x08\n\x02&\x0c\x16\x05=\t\x0c\x16\x0b\x16\x0c\x14\x0b\x14\x03B\x05G\n\x08\n\x01\x0c\x18\x0c\x17\x05I\x06\xbf\x0f\x00\x00\x00\x00\x00\x00\'\x0b\x17\x0b\x18\x0c\x1a\x0c\x19\x0b\x19\x0b\x1a\x0c\t\x0c\x07\n\x075\x0c\x0b\n\t5\x0c\x0c\n\x065\x0c\x0f\n\x045\x0c\r\n\x055\x0c\x0e\n\x06\x06\x00\x00\x00\x00\x00\x00\x00\x00!\x03e\x05j\n\x07\n\t\x11\x18\x0c\x1b\x05v\n\x0b\n\x0f\x18\n\r\x1a\n\x0c\n\x0f\x18\n\x0e\x1a\x11\x15\x0c\x1b\x0b\x1b\x0c\x10\n\x10\x06\x00\x00\x00\x00\x00\x00\x00\x00$\x0c\x1c\x0b\x1c\x03\x7f\x05\x83\x01\n\x10\n\x07\n\t\x02\x06\xc0\x0f\x00\x00\x00\x00\x00\x00\'\x15\x00\x00\x03\x0e\n\x00\n\x01#\x03\x05\x05\t\n\x004\x0c\x02\x05\x0c\n\x014\x0c\x02\x0b\x02\x02\x16\x00\x00\x1f)\n\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00$\x03\x05\x05\n\n\x01\x06\x00\x00\x00\x00\x00\x00\x00\x00$\x0c\x06\x05\x0c\t\x0c\x06\x0b\x06\x03\x0f\x05\x14\n\x02\x06\x00\x00\x00\x00\x00\x00\x00\x00$\x0c\x07\x05\x16\t\x0c\x07\x0b\x07\x0c\x04\x0b\x04\x03\x1b\x05\'\n\x005\n\x025\x18\n\x015\x1a4\x0c\x03\n\x03\x02\x06\xc8\x0f\x00\x00\x00\x00\x00\x00\'\x17\x00\x00\x01\x02\x07\x01\x02\x18\x00\x00 0\n\x005\n\x015\x18\x0c\x032\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x04\n\x032\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00$\x03\r\x05&\n\x03\x0c\x04\n\x032\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1a2\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x16\x0c\x02\n\x02\n\x04#\x03\x1a\x05%\n\x02\x0c\x04\n\x03\n\x02\x1a\n\x02\x162\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1a\x0c\x02\x05\x15\x05-\n\x032\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"\x03+\x05-2\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x04\n\x044\x02\x19\x01\x01\x00!%\x11\x17<\x00\x0c\x05\n\x05.8\x01\n\x03&\x0c\x07\x0b\x07\x03\x0c\x05\x1d\x0b\x056\x00\n\x038\x06\x0c\x06\x0b\x00\x11\x17\x0b\x068\x07\x0b\x02\x10\x01\n\x01\n\x03\x0b\x04\x07\x008\x08\x02\x0b\x02\x01\x0b\x05\x01\x0b\x00\x01\x06\xb4\x0f\x00\x00\x00\x00\x00\x00\'\x00\x00\x04\x00\x00\x1b\x00',
    "add_currency": b'\xa1\x1c\xeb\x0b\x01\x00\x06\x01\x00\x06\x03\x06\x17\x04\x1d\x06\x05#\x0b\x07.F\x08t \x00\x00\x01\x01\x01\x02\x00\x03\x00\x01\x01\x01\x02\x04\x00\x02\x00\x01\x05\x02\x03\x01\x01\x01\x03\x00\x01\x01\x01\x00\x04\x02\x04\x03\x04\x01\x06\x0c\x00\x01\x05\x01\x01\x01\t\x00\x08Exchange\x0cLibraAccount\x06Signer\x0cadd_currency\naddress_of\x10accepts_currencyrW\xc2A~M\x108\xe1\x81|\x8f(:\xce.\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x01\x00\x01\x0e\n\x008\x00\n\x00\x11\x018\x01 \x03\x08\x05\x0b\x0b\x008\x02\x05\r\x0b\x00\x01\x02',
    "add_liquidity": b'\xa1\x1c\xeb\x0b\x01\x00\x06\x01\x00\x02\x03\x02\x07\x04\t\x02\x05\x0b\r\x07\x18\x17\x08/\x10\x00\x00\x00\x01\x00\x01\x02\x01\x01\x00\x02\x05\x06\x0c\x03\x03\x03\x03\x00\x02\t\x00\t\x01\x08Exchange\radd_liquidityrW\xc2A~M\x108\xe1\x81|\x8f(:\xce.\x02\x01\x01\x00\x01\x07\x0b\x00\n\x01\n\x02\n\x03\n\x048\x00\x02',
    "initialize": b'\xa1\x1c\xeb\x0b\x01\x00\x05\x01\x00\x02\x03\x02\x05\x05\x07\x04\x07\x0b\x14\x08\x1f\x10\x00\x00\x00\x01\x00\x01\x00\x01\x06\x0c\x00\x08Exchange\ninitializerW\xc2A~M\x108\xe1\x81|\x8f(:\xce.\x00\x00\x01\x03\x0b\x00\x11\x00\x02',
    "remove_liquidity": b'\xa1\x1c\xeb\x0b\x01\x00\x06\x01\x00\x02\x03\x02\x07\x04\t\x02\x05\x0b\x0c\x07\x17\x1a\x081\x10\x00\x00\x00\x01\x00\x01\x02\x01\x01\x00\x02\x04\x06\x0c\x03\x03\x03\x00\x02\t\x00\t\x01\x08Exchange\x10remove_liquidityrW\xc2A~M\x108\xe1\x81|\x8f(:\xce.\x02\x01\x01\x00\x01\x06\x0b\x00\n\x01\n\x02\n\x038\x00\x02',
    "swap": b'\xa1\x1c\xeb\x0b\x01\x00\x06\x01\x00\x02\x03\x02\x07\x04\t\x02\x05\x0b\x10\x07\x1b\x0e\x08)\x10\x00\x00\x00\x01\x00\x01\x02\x01\x01\x00\x02\x06\x06\x0c\x05\x03\x03\n\x02\n\x02\x00\x02\t\x00\t\x01\x08Exchange\x04swaprW\xc2A~M\x108\xe1\x81|\x8f(:\xce.\x02\x01\x01\x00\x01\x08\x0b\x00\n\x01\n\x02\n\x03\x0b\x04\x0b\x058\x00\x02',
}

type_to_code_map = {
    CodeType.EXCHANGE: bytecodes["exchange"],
    CodeType.EXDEP: bytecodes["exdep"],
    CodeType.ADD_CURRENCY: bytecodes["add_currency"],
    CodeType.ADD_LIQUIDITY: bytecodes["add_liquidity"],
    CodeType.INITIALIZE: bytecodes["initialize"],
    CodeType.REMOVE_LIQUIDITY: bytecodes["remove_liquidity"],
    CodeType.SWAP: bytecodes["swap"],
}

hash_to_type_map = { gen_hex_hash(v): k for k, v in type_to_code_map.items()}

default_module_address = bytes.fromhex("7257c2417e4d1038e1817c8f283ace2e")
current_module_address = default_module_address


def update_hash_to_type_map(module_address):
    global hash_to_type_map
    global current_module_address
    module_address = AccountAddress.normalize_to_bytes(module_address)
    hash_to_type_map = { gen_hex_hash(v.replace(default_module_address, module_address)): k for k, v in type_to_code_map.items()}
    current_module_address = module_address

def get_code_type(code_hash: bytes, module_address=None):
    if isinstance(code_hash, bytes):
        code_hash = code_hash.hex()
    m = hash_to_type_map
    if module_address:
        module_address = AccountAddress.normalize_to_bytes(module_address)
        m = {gen_hex_hash(v.replace(default_module_address, module_address)): k for k, v in
                            type_to_code_map.items()}
    type = m.get(code_hash)
    if type is not None:
        return type
    return LibraCodeType.UNKNOWN


def get_code(type, module_address=None):
    code = type_to_code_map.get(type)
    if code is not None:
        if module_address:
            module_address = AccountAddress.normalize_to_bytes(module_address)
            code = code.replace(default_module_address, module_address)
        return code

def gen_code_type():
    for index, key in enumerate(bytecodes.keys()):
        print(f"{key.upper()} = {index+1000}")

def gen_type_to_code_map():
    for key in bytecodes.keys():
        print(f'CodeType.{key.upper()}: bytecodes["{key}"],')


if __name__ == "__main__":
    print(get_code_type("4302069de7cd03f8975484333f0474b3e16075a75d9b5e8ea4504daf18674177"))
    print(hash_to_type_map)
    # gen_code_type()
    # gen_type_to_code_map()