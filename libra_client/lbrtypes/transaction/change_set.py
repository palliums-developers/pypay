from libra_client.canoser import Struct
from libra_client.lbrtypes.contract_event import ContractEvent
from libra_client.lbrtypes.write_set import WriteSet

class ChangeSet(Struct):
    _fields = [
        ("write_set", WriteSet),
        ("events", [ContractEvent])
    ]
