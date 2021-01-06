from libra_client.canoser import Struct, Uint64
from libra_client.move_core_types.move_resource import MoveResource

class PreburnResource(Struct, MoveResource):
    MODULE_NAME = "Libra"
    STRUCT_NAME = "Preburn"

    _fields = [
        ("coin", Uint64)
    ]