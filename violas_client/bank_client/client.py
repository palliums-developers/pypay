from violas_client.libra_client import Client as LibraClient
from violas_client.banktypes.transaction.module import Module
from violas_client.banktypes.transaction.script import Script
from violas_client.banktypes.view import TransactionView
from violas_client.banktypes.bytecode import CodeType
from violas_client.banktypes.account_state import AccountState
from violas_client.lbrtypes.transaction.transaction_argument import TransactionArgument
from violas_client.lbrtypes.rustlib import ensure
from violas_client.banktypes.bytecode import update_hash_to_type_map
from typing import Optional
from violas_client.error import LibraError
from violas_client.banktypes.bank_error import BankError
from violas_client.move_core_types.language_storage import core_code_address
from violas_client.banktypes.utils import mantissa_div, mantissa_mul

class Client(LibraClient):

    BANK_OWNER_ADDRESS = "00000000000000000000000042414e4b"
    BANK_MODULE_ADDRESS = core_code_address()
    DEFAULT_GAS_COIN_NAME = "VLS"

    def bank_publish_module(self, sender_account, is_blocking=True, **kwargs):
        module = Module.gen_module(module_address=sender_account.address)
        return self.submit_module(sender_account, module, is_blocking, **kwargs)

    def bank_update_price_from_oracle(self, sender_account, currency_code, is_blocking=True, **kwargs):
        args = []
        ty_args = self.get_type_args(currency_code)
        script = Script.gen_script(CodeType.UPDATE_PRICE_FROM_ORACLE, *args, ty_args=ty_args, module_address=self.get_bank_module_address())
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def bank_register_token(self, sender_account, currency_code, price_oracle, collater_factor, base_rate, rate_multiplier, rate_jump_mutiplier, rate_kink, data=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_address(price_oracle))
        args.append(TransactionArgument.to_U64(int(collater_factor*(2**32))))
        args.append(TransactionArgument.to_U64(int(base_rate*(2**32)*60*24*30)))
        args.append(TransactionArgument.to_U64(int(rate_multiplier*(2**32)*60*24*30)))
        args.append(TransactionArgument.to_U64(int(rate_jump_mutiplier*(2**32)*60*24*30)))
        args.append(TransactionArgument.to_U64(int(rate_kink*(2**32))))
        args.append(TransactionArgument.to_U8Vector(data, hex=False))

        ty_args = self.get_type_args(currency_code)
        script = Script.gen_script(CodeType.REGISTER_LIBRA_TOKEN, *args, ty_args=ty_args, module_address=self.get_bank_module_address())
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def bank_borrow(self, sender_account, amount,  currency_code, data=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(amount))
        args.append(TransactionArgument.to_U8Vector(data, hex=False))

        ty_args = self.get_type_args(currency_code)
        script = Script.gen_script(CodeType.BORROW, *args, ty_args=ty_args, module_address=self.get_bank_module_address())
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def bank_borrow2(self, sender_account, amount,  currency_code, data=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(amount))
        args.append(TransactionArgument.to_U8Vector(data, hex=False))

        ty_args = self.get_type_args(currency_code)
        script = Script.gen_script(CodeType.BORROW2, *args, ty_args=ty_args, module_address=self.get_bank_module_address())
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def bank_lock(self, sender_account, amount, currency_code, data=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(amount))
        args.append(TransactionArgument.to_U8Vector(data, hex=False))

        ty_args = self.get_type_args(currency_code)
        script = Script.gen_script(CodeType.LOCK, *args, ty_args=ty_args, module_address=self.get_bank_module_address())
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def bank_lock2(self, sender_account, amount, currency_code, data=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(amount))
        args.append(TransactionArgument.to_U8Vector(data, hex=False))

        ty_args = self.get_type_args(currency_code)
        script = Script.gen_script(CodeType.LOCK2, *args, ty_args=ty_args, module_address=self.get_bank_module_address())
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def bank_publish(self, sender_account, data=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U8Vector(data, hex=False))
        script = Script.gen_script(CodeType.PUBLISH, *args, ty_args=[], module_address=self.get_bank_module_address())
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def bank_redeem(self, sender_account, amount, currency_code, data=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(amount))
        args.append(TransactionArgument.to_U8Vector(data, hex=False))

        ty_args = self.get_type_args(currency_code)
        script = Script.gen_script(CodeType.REDEEM, *args, ty_args=ty_args, module_address=self.get_bank_module_address())
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def bank_redeem2(self, sender_account, amount, currency_code, data=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(amount))
        args.append(TransactionArgument.to_U8Vector(data, hex=False))

        ty_args = self.get_type_args(currency_code)
        script = Script.gen_script(CodeType.REDEEM2, *args, ty_args=ty_args, module_address=self.get_bank_module_address())
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def bank_repay_borrow(self, sender_account, amount, currency_code, data=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(amount))
        args.append(TransactionArgument.to_U8Vector(data, hex=False))

        ty_args = self.get_type_args(currency_code)
        script = Script.gen_script(CodeType.REPAY_BORROW, *args, ty_args=ty_args, module_address=self.get_bank_module_address())
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def bank_repay_borrow2(self, sender_account, amount, currency_code, data=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(amount))
        args.append(TransactionArgument.to_U8Vector(data, hex=False))

        ty_args = self.get_type_args(currency_code)
        script = Script.gen_script(CodeType.REPAY_BORROW2, *args, ty_args=ty_args, module_address=self.get_bank_module_address())
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def bank_liquidate_borrow(self, sender_account, borrower, borrowed_currency, collateral_currency, amount, data=None, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_address(borrower))
        args.append(TransactionArgument.to_U64(amount))
        args.append(TransactionArgument.to_U8Vector(data, hex=False))

        ty_args = self.get_type_args(borrowed_currency)
        ty_args.extend(self.get_type_args(collateral_currency))
        script = Script.gen_script(CodeType.LIQUIDATE_BORROW, *args, ty_args=ty_args, module_address=self.get_bank_module_address())
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def bank_enter(self, sender_account, amount, currency_code, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(amount))

        ty_args = self.get_type_args(currency_code)
        script = Script.gen_script(CodeType.ENTER_BANK, *args, ty_args=ty_args,
                                   module_address=self.get_bank_module_address())
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def bank_exit(self, sender_account, amount, currency_code, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(amount))

        ty_args = self.get_type_args(currency_code)
        script = Script.gen_script(CodeType.EXIT_BANK, *args, ty_args=ty_args,
                                   module_address=self.get_bank_module_address())
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def bank_update_collateral_factor(self, sender_account, currency_code, factor, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(int(factor*(2**32))))

        ty_args = self.get_type_args(currency_code)
        script = Script.gen_script(CodeType.UPDATE_COLLATERAL_FACTOR, *args, ty_args=ty_args,
                                   module_address=self.get_bank_module_address())
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def bank_update_rate_model(self, sender_account, currency_code, base_rate, rate_multiplier, rate_jump_multiplier, rate_kink, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(int(base_rate*(2**32)*60*24*30)))
        args.append(TransactionArgument.to_U64(int(rate_multiplier*(2**32)*60*24*30)))
        args.append(TransactionArgument.to_U64(int(rate_jump_multiplier*(2**32)*60*24*30)))
        args.append(TransactionArgument.to_U64(int(rate_kink*(2**32))))

        ty_args = self.get_type_args(currency_code)

        script = Script.gen_script(CodeType.UPDATE_RATE_MODEL, *args, ty_args=ty_args, module_address=self.get_bank_module_address())
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def claim_incentive(self, sender_account, is_blocking=True, **kwargs):
        args = []
        ty_args = []
        script = Script.gen_script(CodeType.CLAIM_INCENTIVE, *args, ty_args=ty_args, module_address=self.get_bank_module_address())
        return self.submit_script(sender_account, script, is_blocking, **kwargs)

    def get_account_blob(self, account_address, from_version=None, to_version=None) -> Optional[AccountState]:
        blob = super().get_account_blob(account_address, from_version, to_version)
        if blob:
            state = AccountState.new(blob)
            state.set_bank_module_address(self.get_bank_module_address())
            return state

    def get_account_state(self, account_address, from_version=None, to_version=None) -> Optional[AccountState]:
        blob = super().get_account_blob(account_address, from_version, to_version)
        if blob:
            state = AccountState.new(blob)
            state.set_bank_module_address(self.get_bank_module_address())
            return state

    def get_transaction(self, version, fetch_events:bool=True) -> Optional[TransactionView]:
        txs = self.get_transactions(version, 1, fetch_events)
        if len(txs):
            return txs[0]

    def get_transactions(self, start_version: int, limit: int, fetch_events: bool=True) -> [TransactionView]:
        txs = super().get_transactions(start_version, limit, fetch_events)
        return [TransactionView.new(tx) for tx in txs]

    def get_account_transaction(self, account_address, sequence_number: int, fetch_events: bool=True) -> TransactionView:
        tx = super().get_account_transaction(account_address, sequence_number, fetch_events)
        if tx:
            return TransactionView.new(tx)

    @LibraClient.return_when_error(0)
    def bank_get_amount(self, account_address, currency_code):
        index = self.bank_get_currency_index(currency_code)
        state = self.get_account_state(account_address)
        return state.get_bank_amount(index)

    @LibraClient.return_when_error({})
    def bank_get_amounts(self, account_address):
        state = self.get_account_state(account_address)
        tokens = state.get_tokens_resource()
        result = {}
        if tokens:
            for token in tokens.ts:
                if token.index % 2 == 0:
                    currency_code = self.bank_get_currency_code(token.index)
                    value = token.value
                    result[currency_code] = value
        return result

    @LibraClient.return_when_error(0)
    def bank_get_lock_amount(self, account_address, currency_code):
        bank_owner_address = self.get_bank_owner_address()
        state = self.get_account_state(bank_owner_address)
        index = state.get_currency_index(currency_code)
        exchange_rate = state.get_exchange_rate(index)
        state = self.get_account_state(account_address)
        return state.get_lock_amount(index, exchange_rate)

    @LibraClient.return_when_error({})
    def bank_get_lock_amounts(self, account_address):
        bank_owner_address = self.get_bank_owner_address()
        owner_state = self.get_account_state(bank_owner_address)
        state = self.get_account_state(account_address)
        tokens = state.get_tokens_resource()
        result = {}
        if tokens:
            for token in tokens.ts:
                if token.index % 2:
                    index = token.index -1
                    exchange_rate = owner_state.get_exchange_rate(index)
                    amount = state.get_lock_amount(index, exchange_rate)
                    currency_code = self.bank_get_currency_code(index)
                    result[currency_code] = amount
        return result

    @LibraClient.return_when_error(0)
    def bank_get_borrow_amount(self, account_address, currency_code):
        bank_owner_address = self.get_bank_owner_address()
        state = self.get_account_state(bank_owner_address)
        index = state.get_currency_index(currency_code)
        interest_index = state.get_borrow_interest(index)
        state = self.get_account_state(account_address)
        return state.get_borrow_amount(index, interest_index)

    @LibraClient.return_when_error({})
    def bank_get_borrow_amounts(self, account_address):
        bank_owner_address = self.get_bank_owner_address()
        owner_state = self.get_account_state(bank_owner_address)
        state = self.get_account_state(account_address)
        tokens = state.get_tokens_resource()
        result = {}
        if tokens:
            for index, borrow in enumerate(tokens.borrows):
                if index % 2 == 0:
                    interest_index = owner_state.get_borrow_interest(index)
                    amount = state.get_borrow_amount(index, interest_index)
                    currency_code = self.bank_get_currency_code(index)
                    result[currency_code] = amount
        return result

    @LibraClient.return_when_error(0)
    def bank_get_total_collateral_value(self, account_address):
        bank_owner_address = self.get_bank_owner_address()
        owner_state = self.get_account_state(bank_owner_address)
        state = self.get_account_state(account_address)
        tokens = state.get_tokens_resource()
        result = {}
        if tokens:
            for token in tokens.ts:
                if token.index % 2:
                    index = token.index - 1
                    exchange_rate = owner_state.get_exchange_rate(index)
                    amount = state.get_lock_amount(index, exchange_rate)
                    currency_code = self.bank_get_currency_code(index)
                    result[currency_code] = amount
        token_info_stores = owner_state.get_token_info_store_resource()
        sum = 0
        for currency, amount in result.items():
            sum += mantissa_mul(mantissa_mul(amount, token_info_stores.get_price(currency)), token_info_stores.get_collateral_factor(currency))
        return sum

    @LibraClient.return_when_error(0)
    def bank_get_total_borrow_value(self, account_address):
        bank_owner_address = self.get_bank_owner_address()
        owner_state = self.get_account_state(bank_owner_address)
        state = self.get_account_state(account_address)
        tokens = state.get_tokens_resource()
        result = {}
        if tokens:
            for index, borrow in enumerate(tokens.borrows):
                if index % 2 == 0:
                    interest_index = owner_state.get_borrow_interest(index)
                    amount = state.get_borrow_amount(index, interest_index)
                    currency_code = self.bank_get_currency_code(index)
                    result[currency_code] = amount
        token_info_stores = owner_state.get_token_info_store_resource()
        sum = 0
        for currency, amount in result.items():
            sum += mantissa_mul(amount[1], token_info_stores.get_price(currency))
        return sum

    @LibraClient.return_when_error(0)
    def bank_get_max_borrow_amount(self, account_address, currency_code):
        bank_owner_address = self.get_bank_owner_address()
        owner_state = self.get_account_state(bank_owner_address)
        state = self.get_account_state(account_address)
        tokens = state.get_tokens_resource()
        result = {}
        if tokens:
            for token in tokens.ts:
                if token.index % 2:
                    index = token.index - 1
                    exchange_rate = owner_state.get_exchange_rate(index)
                    amount = state.get_lock_amount(index, exchange_rate)
                    currency = self.bank_get_currency_code(index)
                    result[currency] = amount
        token_info_stores = owner_state.get_token_info_store_resource()
        sum = 0
        for currency, amount in result.items():
            sum += mantissa_mul(mantissa_mul(amount, token_info_stores.get_price(currency)),
                                   token_info_stores.get_collateral_factor(currency))

        result = {}
        if tokens:
            for index, borrow in enumerate(tokens.borrows):
                if index % 2 == 0:
                    interest_index = owner_state.get_borrow_interest(index)
                    amount = state.get_borrow_amount(index, interest_index)
                    currency = self.bank_get_currency_code(index)
                    result[currency] = amount
        token_info_stores = owner_state.get_token_info_store_resource()
        for currency, amount in result.items():
            sum -= mantissa_mul(amount[1], token_info_stores.get_price(currency))

        if sum <= 0:
            return 0
        return mantissa_div(sum, token_info_stores.get_price(currency_code))

    @LibraClient.return_when_error(0)
    def bank_get_lock_amounts_to_currency(self, account_address, currency_code):
        bank_owner_address = self.get_bank_owner_address()
        owner_state = self.get_account_state(bank_owner_address)
        token_info_resource = owner_state.get_token_info_store_resource()
        lock_amounts = self.bank_get_lock_amounts(account_address)
        borrow_amounts = self.bank_get_borrow_amounts(account_address)
        sum = 0
        for currency, amount in lock_amounts.items():
            sum += token_info_resource.get_price(currency)*amount
        for currency, amount in borrow_amounts.items():
            sum -= token_info_resource.get_price(currency)*amount[1]

        return int(sum / token_info_resource.get_price(currency_code))

    @LibraClient.return_when_error(None)
    def bank_get_sum_incentive_amount(self, account_address):
        bank_owner_address = self.get_bank_owner_address()
        owner_state = self.get_account_state(bank_owner_address)
        tokens = owner_state.get_token_info_store_resource(accrue_interest=False, update_incentive_supply_index=True, update_incentive_borrow_index=True).tokens
        state = self.get_account_state(account_address)
        sum = 0
        for i in range(0, len(tokens), 2):
            sum += state.get_supply_incentive(i, tokens)
            sum += state.get_borrow_incentive(i, tokens)
        return sum

    @LibraClient.return_when_error(None)
    def bank_get_incentive_amount(self, account_address, currency_code):
        index = self.bank_get_currency_index(currency_code)
        bank_owner_address = self.get_bank_owner_address()
        owner_state = self.get_account_state(bank_owner_address)
        tokens = owner_state.get_token_info_store_resource(accrue_interest=False, update_incentive_supply_index=True, update_incentive_borrow_index=True).tokens
        state = self.get_account_state(account_address)
        sum = state.get_supply_incentive(index, tokens) + state.get_borrow_incentive(index, tokens)
        return sum

    def bank_get_lock_rate(self, currency_code):
        bank_owner_address = self.get_bank_owner_address()
        state = self.get_account_state(bank_owner_address)
        return state.get_lock_rate(currency_code)

    def bank_get_borrow_rate(self, currency_code):
        bank_owner_address = self.get_bank_owner_address()
        state = self.get_account_state(bank_owner_address)
        return state.get_borrow_rate(currency_code)

    def bank_get_registered_currencies(self, update=False):
        if update or not hasattr(self, "bank_registered_currencies"):
            return self.bank_update_registered_currencies()
        if hasattr(self, "bank_registered_currencies"):
            return self.bank_registered_currencies

    def get_utilization(self, currency_code):
        state = self.get_account_state(self.get_bank_module_address())
        return state.get_utilization_rate(currency_code)

    @LibraClient.return_when_error(False)
    def bank_is_published(self, account_address):
        return self.get_account_state(account_address).bank_is_published()

    '''....................................called internal.........................................'''
    def bank_update_registered_currencies(self):
        bank_module_address = self.get_bank_module_address()
        bank_owner_address = self.get_bank_owner_address()
        state = self.get_account_state(bank_owner_address)
        if state is not None:
            state.set_bank_module_address(bank_module_address)
            token_info_store = state.get_token_info_store_resource()
            if token_info_store is not None:
                tokens = token_info_store.tokens
                self.bank_registered_currencies = [token.currency_code for index, token in enumerate(tokens) if index % 2==0 ]
                return self.bank_registered_currencies

    def bank_get_currency_index(self, currency_code):
        currency_code = self.parse_currency_code(currency_code)
        registered_currencies = self.bank_get_registered_currencies()
        ensure(registered_currencies is not None, "Registered_currencies is None")
        for index, code in enumerate(registered_currencies):
            if code == currency_code:
                return index*2
        self.bank_update_registered_currencies()
        for index, code in enumerate(registered_currencies):
            if code == currency_code:
                return index*2
        raise LibraError(data=BankError.CURRENCY_NOT_REGISTERED, message=f"Currency {currency_code} not registered")

    def bank_get_currency_code(self, index):
        index = int(index / 2)
        registered_currencies = self.bank_get_registered_currencies()
        ensure(registered_currencies is not None, "Registered currencies is None")
        if len(registered_currencies) <= index:
            self.bank_update_registered_currencies()
        ensure(len(registered_currencies) > index, f"Registered currencies has no id: {index}")
        return registered_currencies[index]

    def set_bank_module_address(self, address):
        self.bank_module_address = address
        update_hash_to_type_map(address)

    def get_bank_module_address(self, address=None):
        if address:
            return address
        if hasattr(self, "bank_module_address"):
            return self.bank_module_address
        return self.BANK_MODULE_ADDRESS

    def set_bank_owner_address(self, address):
        self.bank_owner_address = address

    def get_bank_owner_address(self, address=None):
        if address:
            return address
        if hasattr(self, "bank_owner_address"):
            return self.bank_owner_address
        return self.BANK_OWNER_ADDRESS

    def parse_currency_code(self, currency_code):
        if currency_code is None:
            return 'LBR'
        return currency_code

