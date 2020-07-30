from libra_client.canoser import Struct, Uint64
from libra_client.move_core_types.identifier import Identifier
from libra_client.move_core_types.account_address import AccountAddress
from libra_client.move_core_types.move_resource import MoveResource
from libra_client.lbrtypes.account_config.constants.libra import LIBRA_MODULE_NAME
from libra_client.lbrtypes.account_config.resources.account import AccountResource

ACCOUNT_RECEIVED_EVENT_PATH = AccountResource.resource_path() + b"/received_events_count/"

class ReceivedPaymentEvent(Struct, MoveResource):
    MODULE_NAME = LIBRA_MODULE_NAME
    STRUCT_NAME = "ReceivedPaymentEvent"

    _fields = [
        ("amount", Uint64),
        ("currency_code", Identifier),
        ("sender", AccountAddress),
        ("metadata", bytes),
    ]