from violas_client.canoser import Struct, Uint64
from violas_client.lbrtypes.account_config import MoveResource
from violas_client.move_core_types.language_storage import StructTag, TypeTag

EXCHANGE_MODULE_NAME = "Exchange"

class TokenResource(Struct, MoveResource):
    MODULE_NAME = EXCHANGE_MODULE_NAME
    STRUCT_NAME = "Token"

    _fields = [
        ("index", Uint64),
        ("value", Uint64)
    ]


class ReserveResource(Struct):
    _fields = [
        ("liquidity_total_supply", Uint64),
        ("coina", TokenResource),
        ("coinb", TokenResource),
    ]

    def get_amountA(self):
        return self.coina.value

    def get_amountB(self):
        return self.coinb.value


class ReservesResource(Struct, MoveResource):
    MODULE_NAME = EXCHANGE_MODULE_NAME
    STRUCT_NAME = "Reserves"

    _fields = [
        ("reserves", [ReserveResource])
    ]

class RegisteredCurrenciesResource(Struct, MoveResource):
    MODULE_NAME = EXCHANGE_MODULE_NAME
    STRUCT_NAME = "RegisteredCurrencies"
    _fields = [
        ("currency_codes", [str])
    ]

class TokensResource(Struct, MoveResource):
    MODULE_NAME = EXCHANGE_MODULE_NAME
    STRUCT_NAME = "Tokens"

    _fields = [
        ("tokens", [TokenResource])
    ]

