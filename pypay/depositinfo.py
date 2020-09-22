import sys

from PyQt5.QtCore import QAbstractListModel, Qt, QUrl, QByteArray, QObject, pyqtSignal, pyqtSlot, pyqtProperty, QModelIndex
from PyQt5.QtQml import qmlRegisterType
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView

from pypay.intormodel import IntorEntry, IntorModel
from pypay.questionmodel import QuestionEntry, QuestionModel

class DepositInfo (QObject):
    def __init__(self, dict = None, parent = None):
        QObject.__init__(self, parent)
        if dict is not None:
            self._id = dict['id'] # 产品ID
            self._name = dict['name'] # 产品名称
            self._minimum_amount = dict['minimum_amount'] # 起购金额
            self._quota_limit = dict['quota_limit'] # 每日限额
            self._quota_used = dict['quota_used'] # 已用限额
            self._rate = dict['rate'] # 产品利率

            self._logo = dict['logo']
            self._token_address = dict['token_address'] # 币种地址
            self._token_module = dict['token_module'] # 币种module
            self._token_name = dict['token_name'] # 币种名称
            self._token_show_name = dict['token_show_name'] # 币种显示名称

            self._intorModel = IntorModel() # 产品说明
            for data in dict['intor']:
                intorEntry = IntorEntry(data)
                self._intorModel.append(intorEntry)

            self._questionModel = QuestionModel() # 常见问题
            for data in dict['question']:
                questionEntry = QuestionEntry(data)
                self._questionModel.append(questionEntry)

    # id
    idChanged = pyqtSignal()

    @pyqtProperty(str, notify=idChanged)
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id
        self.idChanged.emit()

    # name
    nameChanged = pyqtSignal()

    @pyqtProperty(str, notify=nameChanged)
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
        self.nameChanged.emit()

    # minimum_amount
    minimum_amountChanged = pyqtSignal()

    @pyqtProperty(int, notify=minimum_amountChanged)
    def minimum_amount(self):
        return self._minimum_amount

    @minimum_amount.setter
    def minimum_amount(self, minimum_amount):
        self._minimum_amount = minimum_amount
        self.minimum_amountChanged.emit()

    # quota_limit 
    quota_limitChanged = pyqtSignal()

    @pyqtProperty(int, notify=quota_limitChanged)
    def quota_limit(self):
        return self._quota_limit

    @quota_limit.setter
    def quota_limit(self, quota_limit):
        self._quota_limit = quota_limit
        self.quota_limitChanged.emit()

    # quota_used
    quota_usedChanged = pyqtSignal()

    @pyqtProperty(int, notify=quota_usedChanged)
    def quota_used(self):
        return self._quota_used

    @quota_used.setter
    def quota_used(self, quota_used):
        self._quota_used = quota_used
        self.quota_usedChanged.emit()

    # rate
    rateChanged = pyqtSignal()

    @pyqtProperty(float, notify=rateChanged)
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, rate):
        self._rate = rate
        self.rateChanged.emit()

    # logo
    logoChanged = pyqtSignal()

    @pyqtProperty(str, notify=logoChanged)
    def logo(self):
        return self._logo

    @logo.setter
    def logo(self, logo):
        self._logo = logo
        self.logoChanged.emit()

    # token_address
    token_addressChanged = pyqtSignal()

    @pyqtProperty(str, notify=token_addressChanged)
    def token_address(self):
        return self._token_address

    @token_address.setter
    def token_address(self, token_address):
        self._token_address = token_address
        self.token_address.emit()

    # token_module
    token_moduleChanged = pyqtSignal()

    @pyqtProperty(str, notify=token_moduleChanged)
    def token_module(self):
        return self._token_module

    @token_module.setter
    def token_module(self, token_module):
        self._token_module = token_module
        self.token_module.emit()

    # token_name
    token_nameChanged = pyqtSignal()

    @pyqtProperty(str, notify=token_nameChanged)
    def token_name(self):
        return self._token_name

    @token_name.setter
    def token_name(self, token_name):
        self._token_name = token_name
        self.token_name.emit()

    # token_show_name
    token_show_nameChanged = pyqtSignal()

    @pyqtProperty(str, notify=token_show_nameChanged)
    def token_show_name(self):
        return self._token_show_name

    @token_show_name.setter
    def token_show_name(self, token_show_name):
        self._token_show_name = token_show_name
        self.token_show_name.emit()

    # intorModel
    @pyqtProperty(QObject, constant=True)
    def intorModel(self):
        return self._intorModel

    # questionModel
    @pyqtProperty(QObject, constant=True)
    def questionModel(self):
        return self._questionModel

    # clear
    @pyqtSlot()
    def clear(self):
        self._id = ''
        self._name = ''
        self._minimum_amount = 0
        self._quota_limit = 0
        self._quota_used = 0
        self._rate = 0

        self._logo = ''
        self._token_address = ''
        self._token_module = ''
        self._token_name = ''
        self._token_show_name = ''

        self._intorModel.clear()
        self._questionModel.clear()
