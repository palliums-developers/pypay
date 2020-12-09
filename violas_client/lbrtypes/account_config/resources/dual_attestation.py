from violas_client.lbrtypes.event import EventHandle
from violas_client.canoser import Struct, Uint64
from violas_client.move_core_types.move_resource import MoveResource


class CredentialResource(Struct, MoveResource):
    MODULE_NAME = "DualAttestation"
    STRUCT_NAME = "Credential"

    _fields = [
        ("human_name", str),
        ("base_url", str),
        ("compliance_public_key", bytes),
        ("expiration_date", Uint64),
        ("compliance_key_rotation_events", EventHandle),
        ("base_url_rotation_events", EventHandle),
    ]