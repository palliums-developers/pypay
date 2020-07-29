from violas_client.canoser import Struct, Uint64
from violas_client.move_core_types.account_address import AccountAddress
from violas_client.move_core_types.move_resource import MoveResource
from violas_client.lbrtypes.on_chain_config import new_epoch_event_key

class NewEpochEvent(Struct, MoveResource):
    MODULE_NAME = "LibraConfig"
    STRUCT_NAME = "NewBlockEvent"

    _fields = [
        ("epoch", Uint64),
    ]

    def get_epoch(self):
        return self.epoch

    def get_event_key(self):
        return self.new_epoch_event_key().hex()