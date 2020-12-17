from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from violas_client import Wallet, Client

class Libra(QObject):
    def __init__(self, client = None, accounts = None, parent=None):
        super().__init__(parent)
        self._client = client
        self._accounts = accounts

    # mint

    @pyqtSlot()
    def requestActiveAccount(self):
        pass
        #try:
        #    self._client.mint_coin(self._accounts[1].address, 500_000,
        #            auth_key_prefix=self._accounts[1].auth_key_prefix, currency_code="LBR")
        #except Exception as result:
        #    print(result)

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
            balances = self._client.get_balances(self._accounts[1].address_hex)
            self.balancesChanged.emit(balances)

        except Exception as result:
            print(result)

    # history

    historyChanged = pyqtSignal(dict)

    @pyqtSlot(dict)
    def requestHistory(self, dt):
        pass
            
    # add cur of account
    @pyqtSlot(str, bool)
    def requestAddCurOfAccount(self, cur, isShow):
        if isShow:
            try:
                self._client.add_currency_to_account(self._accounts[1], cur)
            except Exception as result:
                print(result)
        else:
            pass
