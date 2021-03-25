from violas_client.canoser import Struct, Uint64, Uint128
from violas_client.lbrtypes.account_config import MoveResource, AccountAddress

EXCHANGE_MODULE_NAME = "Exchange"

class RewardAdminResource(Struct, MoveResource):
    MODULE_NAME = EXCHANGE_MODULE_NAME
    STRUCT_NAME = "RewardAdmin"

    _fields = [
        ("addr", AccountAddress),
    ]

class MintEvent(Struct):
    _fields = [
        ("coina", str),
        ("deposit_amounta", Uint64),
        ("coinb", str),
        ("deposit_amountb", Uint64),
        ("mint_amount", Uint64),
    ]

class BurnEvent(Struct):
    _fields = [
        ("coina", str),
        ("withdraw_amounta", Uint64),
        ("coinb", str),
        ("withdraw_amountb", Uint64),
        ("burn_amount", Uint64),
    ]

class SwapEvent(Struct):
    _fields = [
        ("input_name", str),
        ("input_amount", Uint64),
        ("output_name", str),
        ("output_amount", Uint64),
        ("data", bytes)
    ]

class RewardEvent(Struct):
    _fields = [
        ("pool_id", Uint64),
        ("reward_amount", Uint64),
    ]

class Event(Struct):
    _fields = [
        ("etype", Uint64),
        ("data", bytes),
        ("timestamp", Uint64)
    ]
    def get_swap_event(self):
        if self.etype == 1:
            return MintEvent.deserialize(self.data)
        if self.etype == 2:
            return BurnEvent.deserialize(self.data)
        if self.etype == 3:
            return SwapEvent.deserialize(self.data)
        if self.etype == 4:
            return RewardEvent.deserialize(self.data)

class UserInfoResource(Struct):
    _fields = [
        ("amount", Uint64),
        ("reward_debt", Uint64)
    ]

class PoolUserInfoResource(Struct):
    _fields = [
        ("pool_id", Uint64),
        ("user_info", UserInfoResource)
    ]

class PoolUserInfosResource(Struct, MoveResource):
    MODULE_NAME = EXCHANGE_MODULE_NAME
    STRUCT_NAME = "PoolUserInfos"

    _fields = [
        ("pool_user_infos", [PoolUserInfoResource]),
    ]

class PoolInfoResource(Struct):
    _fields = [
        ("id", Uint64),
        ("lp_supply", Uint64),
        ("alloc_point", Uint64),
        ("acc_vls_per_share", Uint128),
    ]

class RewardPoolsResource(Struct, MoveResource):
    MODULE_NAME = EXCHANGE_MODULE_NAME
    STRUCT_NAME = "RewardPools"

    _fields = [
        ("start_time", Uint64),
        ("end_time", Uint64),
        ("last_reward_time", Uint64),
        ("total_reward_balance", Uint64),
        ("reward_per_second", Uint64),
        ("total_alloc_point", Uint64),
        ("pool_infos", [PoolInfoResource]),
    ]


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

