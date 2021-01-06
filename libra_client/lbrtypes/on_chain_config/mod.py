from libra_client.canoser import Struct, Uint64
from libra_client.lbrtypes.event import EventHandle, EventKey
from libra_client.move_core_types.account_address import AccountAddress
from libra_client.move_core_types.move_resource import MoveResource
from libra_client.lbrtypes.access_path import AccessPath
from libra_client.move_core_types.language_storage import StructTag, CORE_CODE_ADDRESS, TypeTag

class ConfigID(Struct):
    _fields = [
        ("adddress", str),
        ("config_name", str)
    ]

    def access_path(self):
        return access_path_for_config(AccountAddress.from_hex(self.adddress), self.config_name)

def config_address() -> AccountAddress:
    return AccountAddress.from_hex("0xA550C18")


class OnChainConfigPayload(Struct):
    _fields = [
        ("epoch", Uint64),
        ("configs", {ConfigID, bytes})
    ]

class OnChainConfig():
    ADDRESS = "0xF1A95"
    IDENTIFIER = ""
    CONFIG_ID = ConfigID(ADDRESS, IDENTIFIER)

    @classmethod
    def resource_path(cls)-> AccessPath:
        return access_path_for_config(cls.ADDRESS, cls.IDENTIFIER)

    @classmethod
    def access_vector(cls):
        return access_vector_for_config(cls.IDENTIFIER)


def new_epoch_event_key() -> EventKey:
    return EventKey.new_from_address(config_address(), 0)

def access_path_for_config(address, config_name: str) -> AccessPath:
    tag = StructTag(
        CORE_CODE_ADDRESS,
        config_name,
        config_name,
        []
    )
    tag = StructTag(
        CORE_CODE_ADDRESS,
        "DiemConfig",
        "DiemConfig",
        [TypeTag("Struct",tag)]
    )
    address = AccountAddress.normalize_to_bytes(address)
    return AccessPath(address, AccessPath.resource_access_vec(tag, []))

def access_vector_for_config(config_name):
    tag = StructTag(
        CORE_CODE_ADDRESS,
        config_name,
        config_name,
        []
    )
    tag = StructTag(
        CORE_CODE_ADDRESS,
        "DiemConfig",
        "DiemConfig",
        [TypeTag("Struct",tag)]
    )
    return tag.access_vector()


class ConfigurationResource(Struct, MoveResource):
    MODULE_NAME = "DiemConfig"
    STRUCT_NAME = "Configuration"

    _fields = [
        ("epoch", Uint64),
        ("last_reconfiguration_time", Uint64),
        ("events", EventHandle)
    ]