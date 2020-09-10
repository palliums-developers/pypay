import copy
from violas_client.extypes.account_state import AccountState as ExchangeAccountState
from violas_client.banktypes.account_state import AccountState as BankAccountState
from violas_client.oracle_client.account_state import AccountState as OracleAccountState

class AccountState(ExchangeAccountState, BankAccountState, OracleAccountState):
    @classmethod
    def new(cls, account_state):
        state = copy.deepcopy(account_state)
        state.__class__ = cls
        return state