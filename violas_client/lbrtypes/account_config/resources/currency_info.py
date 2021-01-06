from violas_client.canoser import Struct, Uint64, Uint128
from violas_client.move_core_types.move_resource import MoveResource
from violas_client.move_core_types.language_storage import StructTag, CORE_CODE_ADDRESS, ResourceKey
from violas_client.lbrtypes.access_path import AccessPath
from violas_client.move_core_types.identifier import Identifier
from violas_client.lbrtypes.event import EventHandle
from violas_client.lbrtypes.account_config import type_tag_for_currency_code, association_address
from violas_client.lbrtypes.access_path import Accesses

class CurrencyInfoResource(Struct, MoveResource):
    MODULE_NAME = "Diem"
    STRUCT_NAME = "CurrencyInfo"

    _fields = [
        ("total_value", Uint128),
        ("preburn_value", Uint64),
        ("to_lbr_exchange_rate", Uint64),
        ("is_synthetic", bool),
        ("scaling_factor", Uint64),
        ("fractional_part", Uint64),
        ("currency_code", Identifier),
        ("can_mint", bool),
        ("mint_events", EventHandle),
        ("burn_events", EventHandle),
        ("preburn_events", EventHandle),
        ("cancel_burn_events", EventHandle),
        ("exchange_rate_update_events", EventHandle)
    ]

    def get_currency_code(self):
        return self.currency_code

    def get_scaling_factor(self):
        return self.scaling_factor

    def get_fractional_part(self):
        return self.fractional_part

    def get_to_lbr_exchange_rate(self):
        return self.to_lbr_exchange_rate / 2**32

    def convert_to_lbr(self, amount):
        mult = amount * self.to_lbr_exchange_rate
        mult >>= 32
        return mult

    @classmethod
    def struct_tag_for(cls, currency_code):
        return StructTag(
            CORE_CODE_ADDRESS,
            CurrencyInfoResource.module_identifier(),
            CurrencyInfoResource.struct_identifier(),
            [type_tag_for_currency_code(currency_code)]
        )

    @classmethod
    def recource_path_for(cls, currency_code):
        resource_key = ResourceKey(association_address(), CurrencyInfoResource.struct_tag_for(currency_code))
        return AccessPath.resource_access_path(resource_key, Accesses.empty())

    @classmethod
    def access_path_for(cls, currency_code):
        return AccessPath.resource_access_vec(CurrencyInfoResource.struct_tag_for(currency_code), Accesses.empty())

    @classmethod
    def access_vector_for(cls, currency_code):
        return CurrencyInfoResource.struct_tag_for(currency_code).access_vector()

