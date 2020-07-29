from PyQt5.QtCore import QAbstractListModel, Qt, QUrl, QByteArray, QObject, pyqtSignal, pyqtSlot, pyqtProperty, QModelIndex
from PyQt5.QtQml import qmlRegisterType
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView

class BitTransactionEntry (QObject):
    def __init__(self, dict, parent = None):
        QObject.__init__(self, parent)
        self._txid = dict['txid']

    # txid
    txidChanged = pyqtSignal()

    @pyqtProperty(str, notify=txidChanged)
    def txid(self):
        return self._txid

    @txid.setter
    def txid(self, txid):
        self._txid = txid
        self.txidChanged.emit()


class BitTransactionModel (QAbstractListModel):
    BitTransactionEntry = Qt.UserRole + 1

    def __init__(self, bitTransactions = None, parent = None):
        QAbstractListModel.__init__(self, parent)
        if bitTransactions is None:
            self._data = []
        else:
            self._data = bitTransactions

    def roleNames(self):
        roles = {
            BitTransactionModel.BitTransactionEntry : QByteArray(b'bitTransactionEntry')
        }
        return roles

    def rowCount(self, index=QModelIndex()):
        return len(self._data)

    def data(self, index, role):
        d = self._data[index.row()]

        if role == BitTransactionModel.BitTransactionEntry:
            #return d['bitTransactionEntry']
            return d
        return None

    def appendBitTransaction(self, bitTransactionEntry):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append(bitTransactionEntry)
        self.endInsertRows()

    def hasTx(self, txid):
        for entry in self._data:
            if entry.txid == txid:
                return True

        return False
