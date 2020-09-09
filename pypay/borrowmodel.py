import sys
from PyQt5.QtCore import QAbstractListModel, Qt, QUrl, QByteArray, QObject, pyqtSignal, pyqtSlot, pyqtProperty, QModelIndex
from PyQt5.QtQml import qmlRegisterType
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView

class BorrowEntry (QObject):
    def __init__(self, dict = None, parent = None):
        QObject.__init__(self, parent)
        if dict is not None:
            self._chain = dict['chain']
            self._name = dict['name']
            self._amount = dict['amount']
            self._totalPrice = dict['totalPrice']
            self._addr = dict['addr']
            self._isDefault = dict['isDefault']
            self._isShow = dict['isShow']
            self._isAddCur = dict['isAddCur']
            self._reate = dict['rate']

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

    # isAddCur
    isAddCurChanged = pyqtSignal()

    @pyqtProperty(bool, notify=isAddCurChanged)
    def isAddCur(self):
        return self._isAddCur

    @isAddCur.setter
    def isAddCur(self, b):
        self._isAddCur = b
        self.isAddCurChanged.emit()

    # rate
    rateChanged = pyqtSignal()

    @pyqtProperty(float, notify=rateChanged)
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, rate):
        self._rate = rate
        self.rateChanged.emit()


class BorrowModel (QAbstractListModel):
    BorrowEntry = Qt.UserRole + 1

    def __init__(self, parent = None):
        QAbstractListModel.__init__(self, parent)
        self._data = []

    def roleNames(self):
        roles = {
            BorrowModel.BorrowEntry : QByteArray(b'borrowEntry')
        }
        return roles

    def rowCount(self, index=QModelIndex()):
        return len(self._data)

    def data(self, index, role):
        d = self._data[index.row()]

        if role == BorrowModel.BorrowEntry:
            return d
        return None

    def append(self, borrowEntry):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append(borrowEntry)
        self.endInsertRows()
