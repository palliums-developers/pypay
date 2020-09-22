from copy import deepcopy
from violas_client.oracle_client.oracle_resource import OracleResource
from violas_client.lbrtypes.account_state import AccountState as LibraAccountState
from violas_client.lbrtypes.account_config.constants.libra import type_tag_for_currency_code

class AccountState(LibraAccountState):

    @classmethod
    def new(cls, account_state: LibraAccountState):
        ret = deepcopy(account_state)
        ret.__class__ = cls
        return ret

    def oracle_get_exchange_rate(self, currency_code):
        currency_type_tag = type_tag_for_currency_code(currency_code)
        resource = self.get(OracleResource.access_path_for(currency_type_tag))
        if resource:
            return OracleResource.deserialize(resource)