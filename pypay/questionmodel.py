import sys
from PyQt5.QtCore import QAbstractListModel, Qt, QUrl, QByteArray, QObject, pyqtSignal, pyqtSlot, pyqtProperty, QModelIndex
from PyQt5.QtQml import qmlRegisterType
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView

class QuestionEntry(QObject):
    def __init__(self, dict = None, parent = None):
        QObject.__init__(self, parent)
        if dict is not None:
            self._tital = dict['tital'] # 标题
            self._text = dict['text'] # 内容

    # desc
    titalChanged = pyqtSignal()

    @pyqtProperty(str, notify=titalChanged)
    def tital(self):
        return self._tital

    @tital.setter
    def tital(self, tital):
        self._tital = tital
        self.titalChanged.emit()

    # text
    textChanged = pyqtSignal()

    @pyqtProperty(str, notify=textChanged)
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        self.textChanged.emit()

class QuestionModel (QAbstractListModel):
    QuestionEntry = Qt.UserRole + 1

    def __init__(self, parent = None):
        QAbstractListModel.__init__(self, parent)
        self._data = []

    def roleNames(self):
        roles = {
            QuestionModel.QuestionEntry : QByteArray(b'questionEntry')
        }
        return roles

    def rowCount(self, index=QModelIndex()):
        return len(self._data)

    def data(self, index, role):
        d = self._data[index.row()]

        if role == QuestionModel.QuestionEntry:
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

