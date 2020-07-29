from violas_client.canoser import Struct, Uint64, Optional
from violas_client.lbrtypes.transaction import Version
from violas_client.crypto.hash import HashValue

Round = Uint64


GENESIS_EPOCH = 0
GENESIS_ROUND = 0
GENESIS_VERSION = 0
GENESIS_TIMESTAMP_USECS = 0


class BlockInfo(Struct):
    from violas_client.lbrtypes.epoch_state import EpochState
    _fields = [
        ("epoch", Uint64),
        ("round", Round),
        ("id", HashValue),
        ("executed_state_id", HashValue),
        ("version", Version),
        ("timestamp_usecs", Uint64),
        ("next_epoch_info", Optional.from_type(EpochState)),
    ]