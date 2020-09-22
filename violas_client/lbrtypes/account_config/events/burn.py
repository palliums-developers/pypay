from violas_client.canoser import Struct, Uint64
from violas_client.move_core_types.identifier import Identifier
from violas_client.move_core_types.account_address import AccountAddress
from violas_client.move_core_types.move_resource import MoveResource
from violas_client.lbrtypes.account_config.constants.libra import LIBRA_MODULE_NAME

class BurnEvent(Struct, MoveResource):
    MODULE_NAME  = LIBRA_MODULE_NAME
    STRUCT_NAME  = "BurnEvent"

    _fields = [
        ("amount", Uint64),
        ("currency_code", Identifier),
        ("preburn_address", AccountAddress),
    ]

    def get_amount(self):
        return self.amount

    def get_currency_code(self):
        return self.currency_code

    def get_preburn_address(self):
        return self.preburn_address.hex()
