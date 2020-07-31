import os
import random
import sys
import pickle
import threading
import qrcode
import qrcode.image
import logging
from violas_client import Wallet, Client
from libra_client import Client as LibraClient
from .tokenmodel import TokenEntry, TokenModel
from .tokentypemodel import TokenTypeModel
from .bittransactionmodel import BitTransactionEntry, BitTransactionModel
from .bitthread import BitThread
from .violasthread import ViolasThread
from .librathread import LibraThread
from .libra import Libra
from .violas import Violas
from .addrbookmodel import AddrBookEntry, AddrBookModel
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty, QUrl, QThread, QTimer
from PyQt5.QtGui import QClipboard, QGuiApplication, QDesktopServices
from mnemonic import Mnemonic
from bip32utils import BIP32Key
from bit import PrivateKeyTestnet, wif_to_key


# 支付控制器
class PayController(QObject):
    def __init__(self, parent = None):
        QObject.__init__(self, parent)
        self._wallet = None
        self._client = None
        self._libraClient = None
        self._mnemonic = ''
        self._mnemonicRandom = ''
        self._mnemonicConfirm = ''
        self._isConfirming = False
        self._addr = ''
        self._tokenModel = TokenModel()
        self._tokenModelData = []
        self._currentTokenEntry = TokenEntry({'chain':'violas', 'name':'LBR', 'amount':0.0000, 'totalPrice':0.00, 'addr':'', 'isDefault':False, 'isShow':False})
        self._tokenTypeModel = TokenTypeModel()
        self._bitKey = None
        self._bitAddr = ''
        self._bitAmount = 0
        self._bitTransactionModel = BitTransactionModel()
        self._currentBitTransactionEntry = BitTransactionEntry({'txid':''})
        self._addrBookModel = AddrBookModel()
        self._addrBookModelData = []
        self._currentSelectedAddr = ''
        self._walletIsCreated = False
        self._isImportWallet = False
        self._timer = QTimer()

    @pyqtSlot()
    def shutdown(self):
        self.saveToFile()

        if self._walletIsCreated == True:
            self._bitThread.stop()
            #self._bitThread.quit()
            self._bitThread.terminate()
            self._bitThread.wait()

            self._lbrThread.quit()
            self._lbrThread.wait()

            self._vlsThread.quit()
            self._vlsThread.wait()

    requestActiveLibraAccount = pyqtSignal()
    requestActiveViolasAccount = pyqtSignal()
    requestLibraCurrencies = pyqtSignal()
    requestViolasCurrencies = pyqtSignal()
    requestLibraBalances = pyqtSignal()
    requestViolasBalances = pyqtSignal()
    requestViolasHistory = pyqtSignal(dict)
    requestLibraHistory = pyqtSignal(dict)

    # 钱包
    @pyqtSlot()
    def createWallet(self):
        fileName = "pypay.wallet"
        isFirstCreateWallet = True
        if os.path.exists(fileName):
            self._wallet = Wallet.recover(fileName)
            isFirstCreateWallet = False
        else:
            self._wallet = Wallet.new()
            account = self._wallet.new_account()
        self._addr = self._wallet.accounts[0].address_hex
        self.addrChanged.emit()
        self._mnemonic = self._wallet.mnemonic
        self.mnemonicChanged.emit()

        # bitcoin testnet
        mnemo = Mnemonic("english")
        entropy = mnemo.to_entropy(self._mnemonic)
        m = BIP32Key.fromEntropy(entropy, False, True)
        wif = m.WalletImportFormat()
        self._bitKey = wif_to_key(wif)
        self._bitAddr = self._bitKey.segwit_address

        self._wallet.write_recovery(fileName)

        self._bitThread = BitThread(self._bitKey, self)
        self._bitThread.balanceChanged.connect(self.updateBitBalance)
        self._bitThread.transactionsChanged.connect(self.updateBitTransactions)
        self._bitThread.start()

        self._client = Client("violas_testnet")
        self._libraClient = LibraClient("libra_testnet")
        if isFirstCreateWallet or self._isImportWallet:
            # 默认币种列表: BTC, LBR, VLS
            self.setDefaultTokens()

        else:
            self.loadFromFile()

        # libra相关操作
        self._lbrThread = QThread(self)
        self._lbr = Libra(self._libraClient, self._wallet.accounts)
        self._lbrThread.finished.connect(self._lbr.deleteLater)
        self.requestActiveLibraAccount.connect(self._lbr.requestActiveAccount)  # active account
        self._lbr.currenciesChanged.connect(self.updateLBRCurrencies)           # currencies
        self.requestLibraCurrencies.connect(self._lbr.requestCurrencies)
        self._lbr.balancesChanged.connect(self.updateLibraBalances)             # balances
        self.requestLibraBalances.connect(self._lbr.requestBalances)
        self._lbr.historyChanged.connect(self.history_libra)                    # history
        self.requestLibraHistory.connect(self._lbr.requestHistory)
        self._lbr.moveToThread(self._lbrThread)
        self._lbrThread.start()

        # violas相关操作
        self._vlsThread = QThread(self)
        self._vls = Violas(self._client, self._wallet.accounts)
        self._vlsThread.finished.connect(self._vls.deleteLater)
        self.requestActiveViolasAccount.connect(self._vls.requestActiveAccount) # active account
        self._vls.currenciesChanged.connect(self.updateVLSCurrencies)           # currencies
        self.requestViolasCurrencies.connect(self._vls.requestCurrencies)
        self._vls.balancesChanged.connect(self.updateViolasBalances)            # balances
        self.requestViolasBalances.connect(self._vls.requestBalances)
        self._vls.historyChanged.connect(self.history_violas)                   # history
        self.requestViolasHistory.connect(self._vls.requestHistory)
        self._vls.moveToThread(self._vlsThread)
        self._vlsThread.start()

        if isFirstCreateWallet:
            self.requestActiveLibraAccount.emit()
            self.requestActiveViolasAccount.emit()

        self._walletIsCreated = True

        self._timer.timeout.connect(self._timeUpdate)
        self._timer.start(1000)

    @pyqtSlot(str)
    def createWalletFromMnemonic(self, mnemonic):
        self._isImportWallet = True
        fileName = "pypay.wallet"
        with open(fileName, 'w') as f:
            f.write(mnemonic + ';1')
        self.createWallet()

    # 助记词
    mnemonicChanged = pyqtSignal()
    @pyqtProperty(str, notify=mnemonicChanged)
    def mnemonic(self):
        return self._mnemonic

    mnemonicRandomChanged = pyqtSignal()
    @pyqtProperty(str, notify=mnemonicRandomChanged)
    def mnemonicRandom(self):
        return self._mnemonicRandom

    mnemonicConfirmChanged = pyqtSignal()
    @pyqtProperty(str, notify=mnemonicConfirmChanged)
    def mnemonicConfirm(self):
        return self._mnemonicConfirm

    # 生成随机助记词
    @pyqtSlot()
    def genMnemonicRandom(self):
        self._mnemonicRandom = ''
        mneList = self._wallet.mnemonic.split(" ")
        random.shuffle(mneList)
        self._mnemonicRandom = ' '.join(mneList)
        self.mnemonicRandomChanged.emit()
        self._isConfirming = False
        self._mnemonicConfirm = ''
        self.mnemonicConfirmChanged.emit()


    # 添加要确认的助记词
    @pyqtSlot(str)
    def addMnemonicWord(self, val):
        if self._isConfirming:
            mneList = self._mnemonicConfirm.split(" ")
            mneList.append(val)
            self._mnemonicConfirm = ' '.join(mneList)
        else:
            self._isConfirming = True
            self._mnemonicConfirm = val
        self.mnemonicConfirmChanged.emit()

    # 地址
    addrChanged = pyqtSignal()
    @pyqtProperty(str, notify=addrChanged)
    def addr(self):
        return self._addr

    # 资产
    def setDefaultTokens(self):
        btcTokenData = {'chain':'bitcoin', 'name':'BTC', 'amount':0, 'totalPrice':0, 'addr':self._bitAddr, 'isDefault':True, 'isShow':True}
        btcTokenEntry = TokenEntry(btcTokenData)
        self._tokenModel.appendToken(btcTokenEntry)
        self._tokenModelData.append(btcTokenData)
        #self._tokenTypeModel.appendTokenType({"type":"BTC"})   // TODO
        lbrTokenData = {'chain':'libra', 'name':'LBR', 'amount':0, 'totalPrice':0, 'addr':self._addr, 'isDefault':True, 'isShow':True}
        lbrTokenEntry = TokenEntry(lbrTokenData)
        self._tokenModel.appendToken(lbrTokenEntry)
        self._tokenModelData.append(lbrTokenData)
        #self._tokenTypeModel.appendTokenType({"type":"LBR"})   // TODO
        vlsTokenData = {'chain':'violas', 'name':'LBR', 'amount':0, 'totalPrice':0, 'addr':self._addr, 'isDefault':True, 'isShow':True}
        vlsTokenEntry = TokenEntry(vlsTokenData)
        self._tokenModel.appendToken(vlsTokenEntry)
        self._tokenModelData.append(vlsTokenData)
        self._tokenTypeModel.appendTokenType({"type":"VLS"})

    @pyqtProperty(QObject, constant=True)
    def tokenModel(self):
        return self._tokenModel

    currentTokenEntryChanged = pyqtSignal()
    @pyqtProperty(TokenEntry, notify=currentTokenEntryChanged)
    def currentTokenEntry(self):
        return self._currentTokenEntry

    @currentTokenEntry.setter
    def currentTokenEntry(self, entry):
        self._currentTokenEntry = entry
        self.currentTokenEntryChanged.emit()

    # 币种类型
    @pyqtProperty(QObject, constant=True)
    def tokenTypeModel(self):
        return self._tokenTypeModel
        
    # 拷贝
    @pyqtSlot(str)
    def copy(self, str):
        cb = QGuiApplication.clipboard()
        cb.setText(str)

    # 更新BTC余额
    @pyqtSlot(float, float)
    def updateBitBalance(self, balance, usdBalance):
        self._tokenModel.changeData({'chain':'bitcoin', 'name':"BTC", 'amount':balance, 'totalPrice':usdBalance})
        for data in self._tokenModelData:
            if data['name'] == 'BTC':
                data['amount'] = balance
                data['totalPrice'] = usdBalance

    # 比特币交易记录
    @pyqtProperty(QObject, constant=True)
    def bitTransactionModel(self):
        return self._bitTransactionModel

    currentBitTransactionEntryChanged = pyqtSignal()
    @pyqtProperty(BitTransactionEntry, notify=currentBitTransactionEntryChanged)
    def currentBitTransactionEntry(self):
        return self._currentBitTransactionEntry

    @currentBitTransactionEntry.setter
    def currentBitTransactionEntry(self, entry):
        self._currentBitTransactionEntry = entry
        self.currentBitTransactionEntryChanged.emit()

    # 更新BTC交易记录
    @pyqtSlot(list)
    def updateBitTransactions(self, transactions):
        for txid in transactions:
            if not self._bitTransactionModel.hasTx(txid):
                self._bitTransactionModel.appendBitTransaction(BitTransactionEntry({'txid':txid}))

    # 打开网页
    @pyqtSlot(str)
    def openUrl(self, url):
        QDesktopServices.openUrl(QUrl(url))

    # 更新Libra账户余额
    @pyqtSlot(dict)
    def updateLibraBalances(self, balances):
        for key, value in balances.items():
            self._tokenModel.changeData({'chain':'libra', 'name':key, 'amount':value, 'totalPrice':0})

    # 更新Violas账户余额
    @pyqtSlot(dict)
    def updateViolasBalances(self, balances):
        for key, value in balances.items():
            self._tokenModel.changeData({'chain':'violas', 'name':key, 'amount':value, 'totalPrice':0})

    # tokenmodel 保存，恢复
    def loadFromFile(self):
        if os.path.exists('pypay.tokenmodel'):
            with open('pypay.tokenmodel', 'rb') as f:
                self._tokenModelData = pickle.load(f)
                for d in self._tokenModelData:
                    entry = TokenEntry(d)
                    self._tokenModel.appendToken(entry)
        if os.path.exists('pypay.addrbookmodel'):
            with open('pypay.addrbookmodel', 'rb') as f:
                self._addrBookModelData = pickle.load(f)
                for d in self._addrBookModelData:
                    entry = AddrBookEntry(d)
                    self._addrBookModel.append(entry)

    def saveToFile(self):
        with open('pypay.tokenmodel', 'wb') as f:
            pickle.dump(self._tokenModelData, f)
        with open('pypay.addrbookmodel', 'wb') as f:
            pickle.dump(self._addrBookModelData, f)

    # 更新是否显示token
    @pyqtSlot(str, bool)
    def updateTokenShow(self, name, isShow):
        for data in self._tokenModelData:
            if data['name'] == name:
                data['isShow'] = isShow

    def updateLBRCurrencies(self, currencies):
        for cur in currencies:
            if not cur=='LBR':
                lbrTokenData = {'chain':'libra', 'name':cur, 'amount':0, 'totalPrice':0, 'addr':self._addr, 'isDefault':False, 'isShow':False}
                lbrTokenEntry = TokenEntry(lbrTokenData)
                self._tokenModel.appendToken(lbrTokenEntry)
                self._tokenModelData.append(lbrTokenData)

    def updateVLSCurrencies(self, currencies):
        for cur in currencies:
            if not cur == 'LBR':
                vlsTokenData = {'chain':'violas', 'name':cur, 'amount':0, 'totalPrice':0, 'addr':self._addr, 'isDefault':False, 'isShow':False}
                vlsTokenEntry = TokenEntry(vlsTokenData)
                self._tokenModel.appendToken(vlsTokenEntry)
                self._tokenModelData.append(vlsTokenData)
                self._tokenTypeModel.appendTokenType({"type":cur})
        
    # 地址薄
    @pyqtProperty(QObject, constant=True)
    def addrBookModel(self):
        return self._addrBookModel

    @pyqtSlot(str, str)
    def addAddrBook(self, name, addr):
        addrBookData = {'name':name, 'addr':addr}
        addrBookEntry = AddrBookEntry(addrBookData)
        self._addrBookModel.append(addrBookEntry)
        self._addrBookModelData.append(addrBookData)

    # 选择的地址薄中的地址
    currentSelectedAddrChanged = pyqtSignal()
    @pyqtProperty(str, notify=currentSelectedAddrChanged )
    def currentSelectedAddr(self):
        return self._currentSelectedAddr
    @currentSelectedAddr.setter
    def currentSelectedAddr(self, addr):
        self._currentSelectedAddr = addr
        self.currentSelectedAddrChanged.emit()

    # 发送
    @pyqtSlot(str, str, str)
    def sendCoin(self, addr, amount, cur):
        amount = int(amount)
        if cur == 'VLS':
            cur = 'LBR'
        self._client.transfer_coin(self._wallet.accounts[0], 
                addr, amount, currency_code=cur)

    # 二维码
    @pyqtSlot(str)
    def genQR(self, token):
        qr = qrcode.QRCode(
                version = 7,
                error_correction = qrcode.constants.ERROR_CORRECT_L,
                box_size = 10,
                border = 4,
                )
        qrURL = 'noknown'
        if token == 'BTC':
            qrURL = 'bitcoin' + ':' + self._bitAddr
        else:
            qrURL = 'violas-' + token + ':' + self._addr
        qr.add_data(qrURL)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        imgFile = 'pypay/qml/icons/qr_{}.png'
        img.save(imgFile.format(token))

    # 交易记录
    @pyqtSlot(dict)
    def history_libra(self, dt):
        print(dt)

    @pyqtSlot(dict)
    def history_violas(self, dt):
        print(dt)

    @pyqtSlot(str, str, int, int, int)
    def requestVLSHistory(self, addr, currency, flows, offset, limit):
        pass

    @pyqtSlot(str, str, int, int, int)
    def requestLBRHistory(self, addr, currency, flows, offset, limit):
        self.requestLibraHistory.emit({'addr':addr, 'currency':None if currency == '' else currency, 
            'flows':None if flows==-1 else flows, 'offset':offset, 'limit':limit})

    # 定时器
    def _timeUpdate(self):
        self.requestLibraCurrencies.emit()
        self.requestViolasCurrencies.emit()
        self.requestLibraBalances.emit()
        self.requestViolasBalances.emit()
