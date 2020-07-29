from PyQt5.QtCore import QAbstractListModel, Qt, QUrl, QByteArray, QObject, pyqtSignal, pyqtSlot, QModelIndex
from PyQt5.QtQml import qmlRegisterType
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView

class TokenTypeModel (QAbstractListModel):
    Type = Qt.UserRole + 1

    def __init__(self, tokenTypes = None, parent = None):
        QAbstractListModel.__init__(self, parent)
        if tokenTypes is None:
            self._data = []
        else:
            self._data = tokenTypes

    def roleNames(self):
        roles = {
            TokenTypeModel.Type : QByteArray(b'type')
        }
        return roles

    def rowCount(self, index=QModelIndex()):
        return len(self._data)

    def data(self, index, role):
        d = self._data[index.row()]

        if role == TokenTypeModel.Type:
            return d['type']
        return None

    def appendTokenType(self, tokenType):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append(tokenType)
        self.endInsertRows()
