from PyQt5.QtCore import pyqtSignal, QThread
from bit import PrivateKeyTestnet

class BitThread(QThread):
    def __init__(self, bitKey = None, parent=None):
        QThread.__init__(self, parent)
        self._bitKey = bitKey

    balanceChanged = pyqtSignal(float, float)
    transactionsChanged = pyqtSignal(list)

    def run(self):
        while not self.isInterruptionRequested():
            try:
                balance = self._bitKey.get_balance('btc')
                usdBalance = self._bitKey.balance_as('usd')
                self.balanceChanged.emit(float(balance), float(usdBalance))
                transactions = self._bitKey.get_transactions()
                self.transactionsChanged.emit(transactions)
                self.sleep(1)
            except Exception as result:
                print(result)

    def stop(self):
        self.requestInterruption()
