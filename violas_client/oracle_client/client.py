from typing import Union, Optional
from violas_client.libra_client import Client as LibraClient
from violas_client.lbrtypes.transaction.transaction_argument import TransactionArgument
from violas_client.oracle_client.bytecodes import gen_script, CodeType
from violas_client.oracle_client.account_state import AccountState
from violas_client.lbrtypes.account_config.constants.lbr import CORE_CODE_ADDRESS

class Client(LibraClient):
    ORACLE_OWNER_ADDRESS = "0000000000000000000000004f524143"
    ORACLE_MODULE_ADDRESS = CORE_CODE_ADDRESS
    DEFAULT_GAS_COIN_NAME = "VLS"

    def update_exchange_rate(self, currency_code, numerator, denominator, is_blocking=True, **kwargs):
        args = []
        args.append(TransactionArgument.to_U64(numerator))
        args.append(TransactionArgument.to_U64(denominator))

        ty_args = self.get_type_args(currency_code)
        script = gen_script(CodeType.UPDATE_EXCHANGE_RATE, *args, ty_args=ty_args)
        return self.submit_script(self.associate_account, script, is_blocking, **kwargs)

    def get_account_state(self, account_address: Union[bytes, str], from_version=None, to_version=None) -> Optional[AccountState]:
        blob = super().get_account_blob(account_address, from_version, to_version)
        if blob:
            state = AccountState.new(blob)
            return state

    def oracle_get_exchange_rate(self, currency_code):
        state = self.get_account_state(self.ORACLE_OWNER_ADDRESS)
        if state is not None:
            return state.oracle_get_exchange_rate(currency_code)

