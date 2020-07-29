from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject
from violas_client import Wallet, Client
import requests

class Libra(QObject):
    def __init__(self, client = None, accounts = None, parent=None):
        QObject.__init__(self, parent)
        self._client = client
        self._accounts = accounts

    historyChanged = pyqtSignal(dict)

    @pyqtSlot(dict)
    def requestHistory(self, dt):
        r = requests.get('https://api4.violas.io/1.0/libra/transaction', params=dt)
        print(r.url)
        if r.status_code == 200:
            self.historyChanged.emit(r.json())
        else:
            print("request error")
