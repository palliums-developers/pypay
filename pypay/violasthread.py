from PyQt5.QtCore import pyqtSignal, QThread

class ViolasThread(QThread):
    def __init__(self, client = None, addr = None, accounts=None, isFirstCreateWallet=False, parent=None):
        QThread.__init__(self, parent)
        self._client = client
        self._addr = addr
        self._isFirstCreateWallet = isFirstCreateWallet
        self._accounts = accounts

    balancesChanged = pyqtSignal(dict)
    currenciesChanged = pyqtSignal(list)

    def initOnChain(self):
        self._client.mint_coin(self._accounts[0].address, 500_000,
                auth_key_prefix=self._accounts[0].auth_key_prefix, currency_code="LBR")
        currencies = self._client.get_registered_currencies()
        self.currenciesChanged.emit(currencies)
        for cur in currencies:
            if not cur == 'LBR':
                try:
                    self._client.add_currency_to_account(self._accounts[0], currency_code=cur)
                except Exception as result:
                    print(result)

    def run(self):
        if self._isFirstCreateWallet:
            self.initOnChain()
        while not self.isInterruptionRequested():
            try:
                balances = self._client.get_balances(self._addr)
                self.balancesChanged.emit(balances)
                self.sleep(1)
            except Exception as result:
                print(result)

    def stop(self):
        self.requestInterruption()
