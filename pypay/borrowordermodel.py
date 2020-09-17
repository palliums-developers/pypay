import sys
from PyQt5.QtCore import QAbstractListModel, Qt, QUrl, QByteArray, QObject, pyqtSignal, pyqtSlot, pyqtProperty, QModelIndex
from PyQt5.QtQml import qmlRegisterType
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView

class BorrowOrderEntry (QObject):
    def __init__(self, dict = None, parent = None):
        QObject.__init__(self, parent)
        if dict is not None:
            self._amount = dict['amount']
            self._id = dict['id']
            self._logo = dict['logo']
            self._name = dict['name']
            self._available_borrow = dict['available_borrow']

    # amount
    amount_changed = pyqtSignal()

    @pyqtProperty(int, notify=amount_changed)
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, amount):
        self._amount = amount
        self.amount_changed.emit()

    # id
    idChanged = pyqtSignal()

    @pyqtProperty(str, notify=idChanged)
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id
        self.idChanged.emit()

    # logo
    logoChanged = pyqtSignal()

    @pyqtProperty(str, notify=logoChanged)
    def logo(self):
        return self._logo

    @logo.setter
    def logo(self, logo):
        self._logo = logo
        self.logoChanged.emit()

    # name
    nameChanged = pyqtSignal()

    @pyqtProperty(str, notify=nameChanged)
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
        self.nameChanged.emit()

    # available_borrow
    available_borrowChanged = pyqtSignal()

    @pyqtProperty(int, notify=available_borrowChanged)
    def available_borrow(self):
        return self._available_borrow

    @available_borrow.setter
    def available_borrow(self, available_borrow):
        self._available_borrow = available_borrow
        self.available_borrow.emit()


class BorrowOrderModel (QAbstractListModel):
    BorrowOrderEntry = Qt.UserRole + 1

    def __init__(self, parent = None):
        QAbstractListModel.__init__(self, parent)
        self._data = []

    def roleNames(self):
        roles = {
            BorrowOrderModel.BorrowOrderEntry : QByteArray(b'borrowOrderEntry')
        }
        return roles

    def rowCount(self, index=QModelIndex()):
        return len(self._data)

    def data(self, index, role):
        d = self._data[index.row()]

        if role == BorrowOrderModel.BorrowOrderEntry:
            return d
        return None

    def append(self, entry):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append(entry)
        self.endInsertRows()

    def clear(self):
        self.beginRemoveRows(QModelIndex(), 0, len(self._data))
        self._data.clear()
        self.endRemoveRows()
