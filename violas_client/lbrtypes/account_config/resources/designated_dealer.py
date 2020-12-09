from violas_client.lbrtypes.event import EventHandle
from violas_client.canoser import Struct, Uint64
from violas_client.move_core_types.move_resource import MoveResource


class DesignatedDealer(Struct, MoveResource):
    MODULE_NAME = "DesignatedDealer"
    STRUCT_NAME = "Dealer"

    _fields = [
        ("received_mint_events", EventHandle),
    ]

