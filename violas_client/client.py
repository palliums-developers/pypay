from typing import Optional, Union
from violas_client.exchange_client import Client as ExchangeClient
from violas_client.bank_client import Client as BankClient
from violas_client.libra_client import Client as LibraClient
from violas_client.vlstypes.account_state import AccountState
from violas_client.vlstypes.view import TransactionView
from violas_client.oracle_client import Client as OracleClient

class Client(ExchangeClient, BankClient, OracleClient, LibraClient):
    DEFAULT_GAS_COIN_NAME = "VLS"

    def get_account_state(self, account_address, from_version=None, to_version=None) -> Optional[AccountState]:
        state = LibraClient.get_account_state(self, account_address, from_version, to_version)
        if state is not None:
            return AccountState.new(state)

    def get_transaction(self, version, fetch_events:bool=True) -> Optional[TransactionView]:
        txs = self.get_transactions(version, 1, fetch_events)
        if len(txs):
            return txs[0]

    def get_transactions(self, start_version: int, limit: int, fetch_events: bool=True) -> [TransactionView]:
        txs = LibraClient.get_transactions(self, start_version, limit, fetch_events)
        return [TransactionView.new(tx) for tx in txs]

    def get_account_transaction(self, account_address: Union[bytes, str], sequence_number: int, fetch_events: bool=True) -> TransactionView:
        tx = LibraClient.get_account_transaction(self, account_address, sequence_number, fetch_events)
        if tx:
            return TransactionView.new(tx)