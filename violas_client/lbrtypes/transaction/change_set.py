from violas_client.canoser import Struct
from violas_client.lbrtypes.contract_event import ContractEvent
from violas_client.lbrtypes.write_set import WriteSet

class ChangeSet(Struct):
    _fields = [
        ("write_set", WriteSet),
        ("events", [ContractEvent])
    ]
