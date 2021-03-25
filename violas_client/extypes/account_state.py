import copy
from typing import Optional
from violas_client.lbrtypes.account_state import AccountState as LibraAccountState
from violas_client.extypes.exchange_resource import ReservesResource, RegisteredCurrenciesResource, TokensResource, RewardPoolsResource, PoolUserInfosResource
from violas_client.move_core_types.language_storage import StructTag, TypeTag
from violas_client.error import get_exception

class AccountState(LibraAccountState):
    @classmethod
    def new(cls, account_state: LibraAccountState):
        ret = copy.deepcopy(account_state)
        ret.__class__ = cls
        return ret

    @get_exception
    def swap_get_reserves_resource(self, exchange_module_address=None) -> Optional[ReservesResource]:
        resource = self.get(ReservesResource.resource_path(module_address=self.get_exchange_module_address(exchange_module_address)))
        return ReservesResource.deserialize(resource).reserves

    @get_exception
    def swap_get_tokens_resource(self, exchange_module_address=None) -> Optional[TokensResource]:
        resource = self.get(TokensResource.resource_path(module_address=self.get_exchange_module_address(exchange_module_address)))
        return TokensResource.deserialize(resource)

    @get_exception
    def swap_get_registered_currencies(self, exchange_module_address=None) -> Optional[RegisteredCurrenciesResource]:
        resource = self.get(RegisteredCurrenciesResource.resource_path(module_address=self.get_exchange_module_address(exchange_module_address)))
        return RegisteredCurrenciesResource.deserialize(resource)

    # @get_exception
    def swap_get_reward_pools(self) -> Optional[RewardPoolsResource]:
        key = RewardPoolsResource.resource_path(module_address=self.get_exchange_module_address())
        resource = self.get(key)
        return RewardPoolsResource.deserialize(resource)

    @get_exception
    def swap_get_pool_user_infos(self) -> Optional[PoolUserInfosResource]:
        key = PoolUserInfosResource.resource_path(module_address=self.get_exchange_module_address())
        resource = self.get(key)
        return PoolUserInfosResource.deserialize(resource)

    @get_exception
    def swap_get_pool_user_info(self, id):
        pool_user_infos = self.swap_get_pool_user_infos()
        p_user_infos = pool_user_infos.pool_user_infos
        for user_info in p_user_infos:
            if user_info.pool_id == id:
                return user_info.user_info

    # @get_exception
    # def swap_get_pool_user_info(self, id, account_address):
    #     pool_user_info = self.swap_get_pool_user_info

    def set_exchange_module_address(self, address):
        if address:
            self.exchange_module_address = address

    def get_exchange_module_address(self, address=None):
        if address:
            return address
        if hasattr(self, "exchange_module_address"):
            return self.exchange_module_address

    def get_type_tag(self, currency_code):
        return TypeTag.new("Struct", StructTag.new(currency_code))

    def type_tags_for_pair(self, coina, coinb):
        taga = TypeTag("Struct", StructTag.new(coina))
        tagb= TypeTag("Struct", StructTag.new(coinb))
        return [taga, tagb]




