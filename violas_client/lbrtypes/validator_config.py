from violas_client.canoser import Struct
from violas_client.move_core_types.move_resource import MoveResource
from violas_client.crypto.ed25519 import Ed25519PublicKey
from violas_client.crypto.x25519 import PublicKey
from violas_client.crypto.multi_ed25519 import Multiaddr
from violas_client.canoser import Optional


class ValidatorConfig(Struct):
    _fields = [
        ("consensus_pubkey", Ed25519PublicKey),
        ("validator_network_identity_public_key", PublicKey),
        ("validator_network_address", Multiaddr),
        ("fullnodes_network_identity_pubkey", PublicKey),
        ("fullnodes_network_address", Multiaddr)
    ]

class ValidatorConfigResource(Struct, MoveResource):
    MODULE_NAME = "ValidatorConfig"
    STRUCT_NAME = "T"
    _fields = [
        ("validator_config", Optional.from_type(ValidatorConfig))
    ]

