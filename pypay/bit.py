from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject
from bit import PrivateKeyTestnet

class Bit(QObject):
    def __init__(self, bitKey = None, parent=None):
        QObject.__init__(self, parent)
        self._bitKey = bitKey

    balanceChanged = pyqtSignal(float, float)
    transactionsChanged = pyqtSignal(list)

    @pyqtSlot()
    def requestBalance(self):
        try:
            balance = self._bitKey.get_balance('btc')
            usdBalance = self._bitKey.balance_as('usd')
            self.balanceChanged.emit(float(balance), float(usdBalance))
        except Exception as result:
            print(result)

    @pyqtSlot()
    def requestTransactions(self):
        try:
            transactions = self._bitKey.get_transactions()
            self.transactionsChanged.emit(transactions)
        except Exception as result:
            print(result)
