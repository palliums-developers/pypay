import copy
import time
from typing import Optional
from violas_client.lbrtypes.account_state import AccountState as LibraAccountState
from violas_client.move_core_types.language_storage import TypeTag, StructTag
from violas_client.banktypes.account_resources import TokensResource, UserInfoResource, TokenInfoStoreResource, LibraTokenResource
from violas_client.error import get_exception
from violas_client.lbrtypes.rustlib import ensure
from .utils import new_mantissa, mantissa_div, mantissa_mul, safe_sub

class AccountState(LibraAccountState):

    @classmethod
    def new(cls, account_state: LibraAccountState):
        ret = copy.deepcopy(account_state)
        ret.__class__ = cls
        return ret

    @get_exception
    def get_tokens_resource(self) -> Optional[TokensResource]:
        resource = self.ordered_map.get(TokensResource.resource_path_for(module_address=self.get_bank_module_address()))
        return TokensResource.deserialize(resource)

    @get_exception
    def get_user_info_resource(self):
        resource = self.ordered_map.get(
            UserInfoResource.resource_path_for(module_address=self.get_bank_module_address()))
        return UserInfoResource.deserialize(resource)

    @get_exception
    def get_token_info_store_resource(self) -> Optional[TokenInfoStoreResource]:
        self.require_bank_account()
        if hasattr(self, "token_info_store"):
            return self.token_info_store
        resource = self.ordered_map.get(
            TokenInfoStoreResource.resource_path_for(module_address=self.get_bank_module_address()))
        resource = TokenInfoStoreResource.deserialize(resource)
        self.token_info_store = resource
        for index in range(0, len(resource.tokens)):
            self._accrue_interest(index)
        return self.token_info_store

    @get_exception
    def get_token_info(self, index):
        token_info_store = self.get_token_info_store_resource()
        return token_info_store.tokens[index]

    @get_exception
    def get_libra_token_resource(self, currency_code):
        self.require_bank_account()
        type_tag = TypeTag("Struct", StructTag.new(module_name=currency_code))
        resource = self.ordered_map.get(
            LibraTokenResource.resource_path_for(type_tag, module_address=self.get_bank_module_address())
        )
        return LibraTokenResource.deserialize(resource)

    @get_exception
    def get_bank_amount(self, index):
        resource = self.get_tokens_resource()
        return resource.ts[index].value

    @get_exception
    def get_lock_amount(self, index, exchange_rate):
        resource = self.get_tokens_resource()
        return mantissa_mul(resource.ts[index+1].value, exchange_rate)

    @get_exception
    def get_borrow_amount(self, index, interest_index):
        borrow_info = self.get_tokens_resource().borrows[index]
        return borrow_info.principal, mantissa_div(mantissa_mul(borrow_info.principal, interest_index), borrow_info.interest_index)

    @get_exception
    def get_borrow_rate(self, currency_code):
        self.require_bank_account()
        index = self.get_currency_index(currency_code)
        return self._borrow_rate(index) / 2**32

    @get_exception
    def get_lock_rate(self, currency_code):
        self.require_bank_account()
        index = self.get_currency_index(currency_code)
        return self._lock_rate(index) / 2**32

    @get_exception
    def get_exchange_rate(self, index):
        self.require_bank_account()
        return self._exchange_rate(index)

    @get_exception
    def get_utilization_rate(self, currency_code):
        self.require_bank_account()
        index = self.get_currency_index(currency_code)
        return self._utilization_rate(index)

    @get_exception
    def get_borrow_interest(self, index):
        self.require_bank_account()
        token_infos = self.get_token_info_store_resource()
        return token_infos.tokens[index].borrow_index
        

    '''.............................called internally......................................'''

    
    def get_currency_index(self, currency_code):
        self.require_bank_account()
        libra_token = self.get_libra_token_resource(currency_code)
        return libra_token.index

    def set_bank_module_address(self, address):
        if address:
            self.bank_module_address = address

    def get_bank_module_address(self, address=None):
        if address:
            return address
        if hasattr(self, "bank_module_address"):
            return self.bank_module_address
        ensure(False, "Not set bank_owner_address")

    def require_bank_account(self):
        resource = self.ordered_map.get(
            TokenInfoStoreResource.resource_path_for(module_address=self.get_bank_module_address()))
        assert(resource is not None)

    def _exchange_rate(self, index):
        self.require_bank_account()
        t = self.get_tokens_resource().ts[index]
        token_infos = self.get_token_info_store_resource()
        ti = token_infos.tokens[index]
        ti1 = token_infos.tokens[index + 1]

        if ti1.total_supply == 0:
            return new_mantissa(1, 100)
        return new_mantissa(t.value + ti.total_borrows - ti.total_reserves, ti1.total_supply)

    def _utilization_rate(self, index):
        self.require_bank_account()
        tokens = self.get_tokens_resource()
        t = tokens.ts[index]
        ti = self.get_token_info_store_resource().tokens[index]
        if ti.total_borrows == 0:
            util = 0
        else:
            util = new_mantissa(ti.total_borrows, ti.total_borrows + safe_sub(t.value, ti.total_reserves))
        return util
    
    def _borrow_rate(self, index):
        util = self._utilization_rate(index)
        ti = self.get_token_info_store_resource().tokens[index]
        if util <= ti.rate_kink:
            return mantissa_mul(ti.rate_multiplier, util) + ti.base_rate
        normalrate = mantissa_mul(ti.rate_multiplier, ti.rate_kink) + ti.base_rate
        excessutil = util - ti.rate_kink
        return mantissa_mul(ti.rate_jump_multiplier, excessutil) + normalrate

    def _lock_rate(self, index):
        util = self._utilization_rate(index)
        borrow_rate = self._borrow_rate(index)
        ti = self.get_token_info_store_resource().tokens[index]
        return mantissa_mul(util, mantissa_mul(borrow_rate, (new_mantissa(100, 100) - new_mantissa(1, 20))))
        # return util*borrow_rate*(0.95)/2**32

    def _accrue_interest(self, index):
        borrowrate = self._borrow_rate(index)
        token_infos = self.get_token_info_store_resource()
        ti = token_infos.tokens[index]
        minute = int(time.time() / 60)
        cnt = safe_sub(minute, ti.last_minute)
        borrowrate = borrowrate*cnt
        ti.last_minute = minute

        interest_accumulated = mantissa_mul(ti.total_borrows, borrowrate)
        ti.total_borrows = ti.total_borrows + interest_accumulated
        reserve_factor = new_mantissa(1, 20)
        ti.total_reserves = ti.total_reserves + mantissa_mul(interest_accumulated, reserve_factor)
        ti.borrow_index = ti.borrow_index + mantissa_mul(ti.borrow_index, borrowrate)

    def _bank_token_2_base(self, amount, exchange_rate, collateral_factor, price):
        value = mantissa_mul(amount, exchange_rate)
        value = mantissa_mul(value, collateral_factor)
        value = mantissa_mul(value, price)
        return value
    
    def _balance_of(self, index):
        tokens = self.get_tokens_resource()
        if index < len(tokens.ts):
            return tokens.ts[index].value
        return 0

    def _borrow_balance_of(self, index, token_infos):
        tokens = self.get_tokens_resource()
        borrow_info = tokens.borrors[index]
        ti = token_infos.tokens[index]
        return mantissa_div(mantissa_mul(borrow_info.principal, ti.borrow_index), borrow_info.interest_index)
    

    def __str__(self):
        import json
        str_amap = super().__str__()
        amap = json.loads(str_amap)
        if hasattr(self, "bank_module_address"):
            tokens_resource = self.get_tokens_resource()
            user_info_resource = self.get_user_info_resource()
            token_info_store_resource = self.get_token_info_store_resource()
            if tokens_resource:
                amap["tokens_resource"] = tokens_resource.to_json_serializable()
            if user_info_resource:
                amap["user_info_resource"] = user_info_resource.to_json_serializable()
            if token_info_store_resource:
                amap["token_info_store_resource"] = token_info_store_resource.to_json_serializable()
        return json.dumps(amap, sort_keys=False, indent=2)




