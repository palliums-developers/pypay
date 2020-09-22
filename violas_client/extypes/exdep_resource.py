from violas_client.canoser import Struct, Uint64, Uint8, RustEnum
from violas_client.lbrtypes.account_config import WithdrawCapabilityResource
from violas_client.lbrtypes.account_config import MoveResource

EXDEP_MODULE_NAME = "ExDep"

class BalanceResource(Struct, MoveResource):
    MODULE_NAME = EXDEP_MODULE_NAME
    STRUCT_NAME = "Balance"

    _fields = [
        ("value", Uint64)
    ]

class WithdrawCapability(Struct):
    _fields = [
        ("cap", WithdrawCapabilityResource)
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

class Event(Struct):
    _fields = [
        ("etype", Uint64),
        ("data", bytes)
    ]
    def get_event(self):
        if self.etype == 1:
            return MintEvent.deserialize(self.data)
        if self.etype == 2:
            return BurnEvent.deserialize(self.data)
        if self.etype == 3:
            return SwapEvent.deserialize(self.data)

