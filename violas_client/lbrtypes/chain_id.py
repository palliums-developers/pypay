from violas_client.canoser import Struct, RustEnum
from enum import IntEnum

class NamedChain(IntEnum):
    MAINNET = 1
    TESTNET = 2
    DEVNET = 3
    TESTING = 4
    PREMAINNET = 5
