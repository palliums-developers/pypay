from libra_client.canoser import Struct, Uint64
from libra_client.lbrtypes.on_chain_config import OnChainConfig

class LibraVersion(Struct, OnChainConfig):
    IDENTIFIER = "LibraVersion"
    _fields = [
        ("major", Uint64)
    ]