from libra_client.canoser import Struct, Uint64
from libra_client.lbrtypes.on_chain_config import OnChainConfig

class DualAttestationLimit(Struct, OnChainConfig):
    IDENTIFIER = "DualAttestationLimit"

    _fields = [
        ("micro_lbr_limit", Uint64)
    ]
