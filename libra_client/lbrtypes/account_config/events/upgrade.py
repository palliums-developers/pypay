from libra_client.canoser import Struct, Uint64
from libra_client.move_core_types.identifier import Identifier
from libra_client.move_core_types.account_address import AccountAddress
from libra_client.move_core_types.move_resource import MoveResource
from libra_client.lbrtypes.account_config.constants.libra import LIBRA_MODULE_NAME
from libra_client.lbrtypes.account_config.resources.account import AccountResource


class UpgradeEvent (Struct, MoveResource):
    MODULE_NAME = "LibraWriteSetManager"
    STRUCT_NAME = "UpgradeEvent"

    _fields = [
        ("write_set", bytes),
    ]