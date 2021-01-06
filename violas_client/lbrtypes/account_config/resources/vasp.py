from violas_client.canoser import Struct, Uint64
from violas_client.move_core_types.move_resource import MoveResource
from violas_client.lbrtypes.account_config.constants import AccountAddress

class ParentVASP(Struct, MoveResource):
    MODULE_NAME = "VASP"
    STRUCT_NAME = "ParentVASP"

    _fields = [
        ("num_children", Uint64),
    ]

class ChildVASP(Struct, MoveResource):
    MODULE_NAME = "VASP"
    STRUCT_NAME = "ChildVASP"

    _fields = [
        ("parent_vasp_addr", AccountAddress)
    ]


