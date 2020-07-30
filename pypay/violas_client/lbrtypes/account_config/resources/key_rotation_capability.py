from violas_client.canoser import Struct, RustOptional
from violas_client.move_core_types.move_resource import MoveResource
from violas_client.lbrtypes.account_config.constants import ACCOUNT_MODULE_NAME, AccountAddress

class KeyRotationCapabilityResource(Struct, MoveResource):
    MODULE_NAME = ACCOUNT_MODULE_NAME
    STRUCT_NAME = "KeyRotationCapability"

    _fields = [
        ("account_address", AccountAddress)
    ]

class KeyRotationCapabilityResourceOption(RustOptional):
    _type = KeyRotationCapabilityResource