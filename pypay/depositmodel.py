import sys
from PyQt5.QtCore import QAbstractListModel, Qt, QUrl, QByteArray, QObject, pyqtSignal, pyqtSlot, pyqtProperty, QModelIndex
from PyQt5.QtQml import qmlRegisterType
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView

class DepositEntry (QObject):
    def __init__(self, dict = None, parent = None):
        QObject.__init__(self, parent)
        if dict is not None:
            self.desc = dict['desc']
            self.id = dict['id']
            self.logo = dict['logo']
            self.name = dict['name']
            self.rate = dict['rate']
            self.rate_desc = dict['rate_desc']
            self.token_module = dict['token_module']

    # desc
    descChanged = pyqtSignal()

    @pyqtProperty(str, notify=descChanged)
    def desc(self):
        return self.desc

    @desc.setter
    def desc(self, desc):
        self.desc = desc
        self.descChanged.emit()

    # id
    idChanged = pyqtSignal()

    @pyqtProperty(str, notify=idChanged)
    def id(self):
        return self.id

    @id.setter
    def id(self, id):
        self.id = id
        self.idChanged.emit()

    # logo
    logoChanged = pyqtSignal()

    @pyqtProperty(str, notify=logoChanged)
    def logo(self):
        return self.logo

    @logo.setter
    def logo(self, logo):
        self.logo = logo
        self.logoChanged.emit()

    # namePrice
    nameChanged = pyqtSignal()

    @pyqtProperty(str, notify=nameChanged)
    def name(self):
        return self.name

    @name.setter
    def name(self, name):
        self.name = name
        self.nameChanged.emit()

    # rate
    rateChanged = pyqtSignal()

    @pyqtProperty(float, notify=rateChanged)
    def rate(self):
        return self.rate

    @rate.setter
    def rate(self, rate):
        self.rate = rate
        self.rateChanged.emit()

    # rate_desc
    rate_descChanged = pyqtSignal()

    @pyqtProperty(str, notify=rate_descChanged)
    def rate_desc(self):
        return self.rate_desc

    @rate_desc.setter
    def rate_desc(self, rate_desc):
        self.rate_desc = rate_desc
        self.rate_descChanged.emit()

    # token_module
    token_moduleChanged = pyqtSignal()

    @pyqtProperty(str, notify=token_moduleChanged)
    def token_module(self):
        return self.token_module

    @token_module.setter
    def token_module(self, token_module):
        self.token_module = token_module
        self.token_module.emit()


class DepositModel (QAbstractListModel):
    DepositEntry = Qt.UserRole + 1

    def __init__(self, parent = None):
        QAbstractListModel.__init__(self, parent)
        self._data = []

    def roleNames(self):
        roles = {
            DepositModel.DepositEntry : QByteArray(b'depositEntry')
        }
        return roles

    def rowCount(self, index=QModelIndex()):
        return len(self._data)

    def data(self, index, role):
        d = self._data[index.row()]

        if role == DepositModel.DepositEntry:
            return d
        return None

    def append(self, depositEntry):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append(depositEntry)
        self.endInsertRows()

    def clear(self):
        self.beginRemoveRows(QModelIndex(), 0, len(self._data))
        self._data.clear()
        self.endRemoveRows()
