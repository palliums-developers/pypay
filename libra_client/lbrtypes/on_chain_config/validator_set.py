from libra_client.canoser import RustEnum, Struct
from libra_client.lbrtypes.validator_info import ValidatorInfo
from libra_client.lbrtypes.on_chain_config import OnChainConfig

from enum import IntEnum

class ConsensusScheme(IntEnum):
    Ed25519 = 0

class ValidatorSet(Struct, OnChainConfig):
    IDENTIFIER = "LibraSystem"

    _field = [
        ("scheme", ConsensusScheme),
        ("payload", [ValidatorInfo]),
    ]