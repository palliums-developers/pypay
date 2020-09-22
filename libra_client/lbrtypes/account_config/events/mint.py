from libra_client.canoser import Struct, Uint64
from libra_client.move_core_types.identifier import Identifier
from libra_client.move_core_types.move_resource import MoveResource
from libra_client.lbrtypes.account_config.constants.libra import LIBRA_MODULE_NAME

class CancelBurnEvent(Struct, MoveResource):
    MODULE_NAME = LIBRA_MODULE_NAME
    STRUCT_NAME = "MintEvent"

    _fields = [
        ("amount", Uint64),
        ("currency_code", Identifier),
    ]

    def get_amount(self):
        return self.amount

    def get_currency_code(self):
        return self.currency_code