import sys
from PyQt5.QtCore import QAbstractListModel, Qt, QUrl, QByteArray, QObject, pyqtSignal, pyqtSlot, pyqtProperty, QModelIndex
from PyQt5.QtQml import qmlRegisterType
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView

class HistoryEntry (QObject):
    def __init__(self, dict = None, parent = None):
        QObject.__init__(self, parent)
        if dict is not None:
            self._amount = dict['amount']
            self._confirmed_time = dict['confirmed_time']
            self._currency = dict['currency']
            self._expiration_time = dict['expiration_time']
            self._gas = dict['gas']
            self._gas_currency = dict['gas_currency']
            self._receiver = dict['receiver']
            self._sender = dict['sender']
            self._sequence_number = dict['sequence_number']
            self._status = dict['status']
            self._type = dict['type']
            self._version = dict['version']

    # amount
    amountChanged = pyqtSignal()

    @pyqtProperty(int, notify=amountChanged)
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, amount):
        self._amount = amount
        self.amountChanged.emit()

    # confirmed_time
    confirmed_timeChanged = pyqtSignal()

    @pyqtProperty(str, notify=confirmed_timeChanged)
    def confirmed_time(self):
        return self._confirmed_time

    @confirmed_time.setter
    def confirmed_time(self, time):
        self._confirmed_time = time
        self.confirmed_timeChanged.emit()

    # currency
    currencyChanged = pyqtSignal()

    @pyqtProperty(str, notify=currencyChanged)
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, cur):
        self._currency = cur
        self.currencyChanged.emit()

    # expiration_time
    expiration_timeChanged = pyqtSignal()

    @pyqtProperty(str, notify=expiration_timeChanged)
    def expiration_time(self):
        return self._expiration_time

    @expiration_time.setter
    def expiration_time(self, time):
        self._expiration_time = time
        self.expiration_timeChanged.emit()

    # gas
    gasChanged = pyqtSignal()

    @pyqtProperty(int, notify=gasChanged)
    def gas(self):
        return self._gas

    @gas.setter
    def gas(self, gas):
        self._gas = gas
        self.gasChanged.emit()

    # gas_currency
    gas_currencyChanged = pyqtSignal()

    @pyqtProperty(str, notify=gas_currencyChanged)
    def gas_currency(self):
        return self._gas_currency

    @gas_currency.setter
    def gas_currency(self, cur):
        self._gas_currency = cur
        self.gas_currencyChanged.emit()

    # receiver
    receiverChanged = pyqtSignal()

    @pyqtProperty(str, notify=receiverChanged)
    def receiver(self):
        return self._receiver

    @receiver.setter
    def receiver(self, rec):
        self._receiver = rec
        self.receiverChanged.emit()

    # sender
    senderChanged = pyqtSignal()

    @pyqtProperty(str, notify=senderChanged)
    def sender(self):
        return self._sender

    @sender.setter
    def sender(self, sen):
        self._sender = sen
        self.senderChanged.emit()

    # sequence_number
    sequence_numberChanged = pyqtSignal()

    @pyqtProperty(int, notify=sequence_numberChanged)
    def sequence_number(self):
        return self._sequence_number

    @sequence_number.setter
    def sequence_number(self, num):
        self._sequence_number = num
        self.sequence_numberChanged.emit()

    # status
    statusChanged = pyqtSignal()

    @pyqtProperty(str, notify=statusChanged)
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status
        self.statusChanged.emit()

    # type
    typeChanged = pyqtSignal()

    @pyqtProperty(str, notify=typeChanged)
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type
        self.typeChanged.emit()

    # version
    versionChanged = pyqtSignal()

    @pyqtProperty(int, notify=versionChanged)
    def version(self):
        return self._version

    @version.setter
    def version(self, ver):
        self._version = ver
        self.versionChanged.emit()


class HistoryModel (QAbstractListModel):
    HistoryEntry = Qt.UserRole + 1

    def __init__(self, parent = None):
        QAbstractListModel.__init__(self, parent)
        self._data = []

    def roleNames(self):
        roles = {
            HistoryModel.HistoryEntry : QByteArray(b'historyEntry')
        }
        return roles

    def rowCount(self, index=QModelIndex()):
        return len(self._data)

    def data(self, index, role):
        d = self._data[index.row()]

        if role == HistoryModel.HistoryEntry:
            return d
        return None

    def append(self, historyEntry):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append(historyEntry)
        self.endInsertRows()

    def clear(self):
        self.beginRemoveRows(QModelIndex(), 0, len(self._data))
        self._data.clear()
        self.endRemoveRows()
