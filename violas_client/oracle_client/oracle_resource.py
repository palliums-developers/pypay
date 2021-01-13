from violas_client.canoser import Struct, Uint64
from violas_client.move_core_types.move_resource import MoveResource
from violas_client.move_core_types.language_storage import StructTag, CORE_CODE_ADDRESS
from violas_client.lbrtypes.access_path import AccessPath
from violas_client.lbrtypes.event import EventHandle

class UpdateEvent(Struct):
    _fields = [
        ("value", Uint64),
        ("timestamp", Uint64),
        ("currency_code", str),
    ]

    def get_value(self):
        return self.value

    def get_timestamp(self):
        return self.timestamp

    def get_currency_code(self):
        return self.currency_code

class OracleResource(Struct, MoveResource):
    MODULE_NAME = "Oracle"
    STRUCT_NAME = "ExchangeRate"

    _fields = [
        ("value", Uint64),
        ("timestamp", Uint64),
        ("update_events", EventHandle),
    ]

    @classmethod
    def struct_tag_for_currency(cls, current_typetag):
        return StructTag(
            CORE_CODE_ADDRESS,
            cls.module_identifier(),
            cls.struct_identifier(),
            [current_typetag]
        )
