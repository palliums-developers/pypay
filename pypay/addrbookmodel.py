import sys
from PyQt5.QtCore import QAbstractListModel, Qt, QUrl, QByteArray, QObject, pyqtSignal, pyqtSlot, pyqtProperty, QModelIndex
from PyQt5.QtQml import qmlRegisterType
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView

class AddrBookEntry (QObject):
    def __init__(self, dict, parent = None):
        QObject.__init__(self, parent)
        self._name = dict['name']
        self._addr = dict['addr']

    # name
    nameChanged = pyqtSignal()

    @pyqtProperty(str, notify=nameChanged)
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
        self.nameChanged.emit()

    # addr
    addrChanged = pyqtSignal()

    @pyqtProperty(str, notify=addrChanged)
    def addr(self):
        return self._addr

    @addr.setter
    def addr(self, addr):
        self._addr = addr
        self.addrChanged.emit()

class AddrBookModel (QAbstractListModel):
    AddrBookEntry = Qt.UserRole + 1

    def __init__(self, parent = None):
        QAbstractListModel.__init__(self, parent)
        self._data = []

    def roleNames(self):
        roles = {
            AddrBookModel.AddrBookEntry : QByteArray(b'addrBookEntry')
        }
        return roles

    def rowCount(self, index=QModelIndex()):
        return len(self._data)

    def data(self, index, role):
        d = self._data[index.row()]

        if role == AddrBookModel.AddrBookEntry:
            #return d['addrBookEntry']
            return d
        return None

    def append(self, addrBookEntry):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append(addrBookEntry)
        self.endInsertRows()

    def changeData(self, name, addr):
        for entry in self._data:
            if entry.name == name:
                entry.addr = addr

