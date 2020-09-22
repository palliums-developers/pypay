from libra_client.canoser import Struct, RustOptional
from libra_client.lbrtypes.transaction import Version
from libra_client.lbrtypes.proof.definition import AccountStateProof
from libra_client.lbrtypes.account_state import AccountState

class AccountStateBlob(Struct):
    _fields = [
        ("blob", AccountState)
    ]

    @classmethod
    def from_proto(cls, proto):
        ret = cls()
        if len(proto.blob) == 0:
            ret.blob = AccountState()
        else:
            ret.blob = AccountState.deserialize(proto.blob)
        return ret

class AccountStateWithProof(Struct):
    _fields = [
        ("version", Version),
        ("blob", AccountStateBlob),
        ("proof", AccountStateProof)
    ]

    def verify(self):
        pass

    def get_event_key_and_count_by_query_path(self):
        pass


