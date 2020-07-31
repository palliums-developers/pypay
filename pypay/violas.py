from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject
from violas_client import Wallet, Client
import requests

class Violas(QObject):
    def __init__(self, client, accounts, parent=None):
        QObject.__init__(self, parent)
        self._client = client
        self._accounts = accounts

    # mint

    @pyqtSlot()
    def requestActiveAccount(self):
        self._client.mint_coin(self._accounts[0].address, 500_000,
                auth_key_prefix=self._accounts[0].auth_key_prefix, currency_code="LBR")

    # currencies

    currenciesChanged = pyqtSignal(list)

    @pyqtSlot()
    def requestCurrencies(self):
        try:
            currencies = self._client.get_registered_currencies()
            self.currenciesChanged.emit(currencies)
        except Exception as result:
            print(result)

    # balances

    balancesChanged = pyqtSignal(dict)

    @pyqtSlot()
    def requestBalances(self):
        try:
            balances = self._client.get_balances(self._accounts[0].address_hex)
            self.balancesChanged.emit(balances)

        except Exception as result:
            print(result)

    # history

    historyChanged = pyqtSignal(dict)

    @pyqtSlot(dict)
    def requestHistory(self, dt):
        r = requests.get('https://api4.violas.io/1.0/violas/transaction', params=dt)
        print(r.url)
        if r.status_code == 200:
            self.historyChanged.emit(r.json())
        else:
            print("request error")
