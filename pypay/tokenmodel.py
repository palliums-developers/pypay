import sys
from PyQt5.QtCore import QAbstractListModel, Qt, QUrl, QByteArray, QObject, pyqtSignal, pyqtSlot, pyqtProperty, QModelIndex
from PyQt5.QtQml import qmlRegisterType
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView

class TokenEntry (QObject):
    def __init__(self, dict, parent = None):
        QObject.__init__(self, parent)
        self._chain = dict['chain']
        self._name = dict['name']
        self._amount = dict['amount']
        self._totalPrice = dict['totalPrice']
        self._addr = dict['addr']
        self._isDefault = dict['isDefault']
        self._isShow = dict['isShow']

    # chain
    chainChanged = pyqtSignal()

    @pyqtProperty(str, notify=chainChanged)
    def chain(self):
        return self._chain

    @chain.setter
    def chain(self, chain):
        self._chain = chain
        self.chainChanged.emit()

    # name
    nameChanged = pyqtSignal()

    @pyqtProperty(str, notify=nameChanged)
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
        self.nameChanged.emit()

    # amount
    amountChanged = pyqtSignal()

    @pyqtProperty(float, notify=amountChanged)
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, amount):
        self._amount = amount
        self.amountChanged.emit()

    # totalPrice
    totalPriceChanged = pyqtSignal()

    @pyqtProperty(float, notify=totalPriceChanged)
    def totalPrice(self):
        return self._totalPrice

    @totalPrice.setter
    def totalPrice(self, price):
        self._totalPrice = price
        self.totalPriceChanged.emit()

    # addr
    addrChanged = pyqtSignal()

    @pyqtProperty(str, notify=addrChanged)
    def addr(self):
        return self._addr

    @addr.setter
    def addr(self, addr):
        self._addr = addr
        self.addrChanged.emit()

    # isDefault
    isDefaultChanged = pyqtSignal()

    @pyqtProperty(bool, notify=isDefaultChanged)
    def isDefault(self):
        return self._isDefault

    @isDefault.setter
    def isDefault(self, b):
        self._isDefault = b
        self.isDefaultChanged.emit()

    # isShow
    isShowChanged = pyqtSignal()

    @pyqtProperty(bool, notify=isShowChanged)
    def isShow(self):
        return self._isShow

    @isShow.setter
    def isShow(self, b):
        self._isShow = b
        self.isShowChanged.emit()


class TokenModel (QAbstractListModel):
    TokenEntry = Qt.UserRole + 1

    def __init__(self, parent = None):
        QAbstractListModel.__init__(self, parent)
        self._data = []

    def roleNames(self):
        roles = {
            TokenModel.TokenEntry : QByteArray(b'tokenEntry')
        }
        return roles

    def rowCount(self, index=QModelIndex()):
        return len(self._data)

    def data(self, index, role):
        d = self._data[index.row()]

        if role == TokenModel.TokenEntry:
            #return d['tokenEntry']
            return d
        return None

    def appendToken(self, tokenEntry):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append(tokenEntry)
        self.endInsertRows()

    def changeData(self, dt):
        for entry in self._data:
            if entry.chain == dt['chain'] and entry.name == dt['name']:
                entry.amount = dt['amount']
                entry.totalPrice = dt['totalPrice']

