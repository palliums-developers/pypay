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
from .bit import Bit
from .libra import Libra
from .violas import Violas
from .addrbookmodel import AddrBookEntry, AddrBookModel
from .historymodel import HistoryEntry, HistoryModel
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
        self._currentTokenEntry = TokenEntry({'chain':'violas', 'name':'LBR', 'amount':0.0000, 'totalPrice':0.00, 'addr':'', 'isDefault':False, 'isShow':False, 'isAddCur':False})
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
        self._historyModel = HistoryModel()
        self._rates = {}
        self._totalBalance = 0

    @pyqtSlot()
    def shutdown(self):
        self._timer.stop()
        self.saveToFile()
        del self._client
        del self._libraClient

#    def __del__(self):
#        if self._walletIsCreated == True:
#            self._bitThread.quit()
#            #self._bitThread.terminate()
#            self._bitThread.wait()
#
#            self._lbrThread.quit()
#            #self._lbrThread.terminate()
#            self._lbrThread.wait()
#
#            self._vlsThread.quit()
#            #self._vlsThread.terminate()
#            self._vlsThread.wait()

    requestBitBalance = pyqtSignal()
    requestBitTransactions = pyqtSignal()
    requestActiveLibraAccount = pyqtSignal()
    requestActiveViolasAccount = pyqtSignal()
    requestLibraCurrencies = pyqtSignal()
    requestViolasCurrencies = pyqtSignal()
    requestLibraBalances = pyqtSignal()
    requestViolasBalances = pyqtSignal()
    requestViolasHistory = pyqtSignal(dict)
    requestLibraHistory = pyqtSignal(dict)
    requestLBRAddCurOfAccount = pyqtSignal(str, bool)
    requestVLSAddCurOfAccount = pyqtSignal(str, bool)
    requestExchangeRates = pyqtSignal()
    requestTotalBalances = pyqtSignal()

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

        self._bitThread = QThread(self)
        self._bit = Bit(self._bitKey)
        self._bitThread.finished.connect(self._bit.deleteLater)
        self.requestBitBalance.connect(self._bit.requestBalance)
        self._bit.balanceChanged.connect(self.updateBitBalance)
        self.requestBitTransactions.connect(self._bit.requestTransactions)
        self._bit.transactionsChanged.connect(self.updateBitTransactions)
        self._bit.moveToThread(self._bitThread)
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
        self.requestLBRAddCurOfAccount.connect(self._lbr.requestAddCurOfAccount)
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
        self.requestVLSAddCurOfAccount.connect(self._vls.requestAddCurOfAccount)
        self.requestExchangeRates.connect(self._vls.requestExchangeRates)
        self._vls.exchangeRatesChanged.connect(self.updateExchangeRates)
        self._vls.moveToThread(self._vlsThread)
        self._vlsThread.start()

        if isFirstCreateWallet:
            self.requestActiveLibraAccount.emit()
            self.requestActiveViolasAccount.emit()

        self._walletIsCreated = True

        self.requestTotalBalances.connect(self.updateTotalBalance)
        self._timer.timeout.connect(self._timeUpdate)
        self._timer.start(5000)

        self.requestExchangeRates.emit()

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

    # btc地址
    btcAddrChanged = pyqtSignal()
    @pyqtProperty(str, notify=btcAddrChanged)
    def btcAddr(self):
        return self._bitAddr

    # 资产
    def setDefaultTokens(self):
        btcTokenData = {'chain':'bitcoin', 'name':'BTC', 'amount':0, 'totalPrice':0, 'addr':self._bitAddr, 'isDefault':True, 'isShow':True, 'isAddCur':True}
        btcTokenEntry = TokenEntry(btcTokenData)
        self._tokenModel.appendToken(btcTokenEntry)
        self._tokenModelData.append(btcTokenData)
        #self._tokenTypeModel.appendTokenType({"type":"BTC"})   // TODO
        lbrTokenData = {'chain':'libra', 'name':'LBR', 'amount':0, 'totalPrice':0, 'addr':self._addr, 'isDefault':True, 'isShow':True, 'isAddCur':True}
        lbrTokenEntry = TokenEntry(lbrTokenData)
        self._tokenModel.appendToken(lbrTokenEntry)
        self._tokenModelData.append(lbrTokenData)
        #self._tokenTypeModel.appendTokenType({"type":"LBR"})   // TODO
        vlsTokenData = {'chain':'violas', 'name':'LBR', 'amount':0, 'totalPrice':0, 'addr':self._addr, 'isDefault':True, 'isShow':True, 'isAddCur':True}
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
            if data['chain'] == 'bitcoin' and data['name'] == 'BTC':
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
        print("libra: ", balances)
        if not balances:
            self.requestActiveLibraAccount.emit()
        for key, value in balances.items():
            amount = value / 1_000_000
            rate = self.getRate(key)
            totalPrice = amount * rate
            print("rate: ", rate)
            self._tokenModel.changeData({'chain':'libra', 'name':key, 'amount':amount, 'totalPrice':totalPrice})
            for data in self._tokenModelData:
                if data['chain'] == 'libra' and data['name'] == key:
                    data['amount'] = amount
                    data['totalPrice'] = totalPrice

    # 更新Violas账户余额
    @pyqtSlot(dict)
    def updateViolasBalances(self, balances):
        print("violas: ", balances)
        if not balances:
            self.requestActiveViolasAccount.emit()
        for key, value in balances.items():
            amount = value / 1_000_000
            rate = self.getRate(key)
            totalPrice = amount * rate
            print("rate: ", rate)
            self._tokenModel.changeData({'chain':'violas', 'name':key, 'amount':amount, 'totalPrice':totalPrice})
            for data in self._tokenModelData:
                if data['chain'] == 'violas' and data['name'] == key:
                    data['amount'] = amount
                    data['totalPrice'] = totalPrice

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

        self.updateTotalBalance()

    def saveToFile(self):
        with open('pypay.tokenmodel', 'wb') as f:
            pickle.dump(self._tokenModelData, f)
        with open('pypay.addrbookmodel', 'wb') as f:
            pickle.dump(self._addrBookModelData, f)

    # 更新是否显示token
    @pyqtSlot(str, str, bool)
    def updateTokenShow(self, chain, name, isShow):
        for data in self._tokenModelData:
            if data['chain'] == chain and data['name'] == name:
                data['isShow'] = isShow
                if isShow == True and data['isAddCur'] == False:
                    data['isAddCur'] = True
                    if chain == 'libra':
                        self.requestLBRAddCurOfAccount.emit(name, True)
                    elif chain == 'violas':
                        self.requestVLSAddCurOfAccount.emit(name, True)
                    else:
                        pass

    def updateLBRCurrencies(self, currencies):
        for cur in currencies:
            if not cur=='LBR':
                if not self._tokenModel.isExist('libra', cur):
                    lbrTokenData = {'chain':'libra', 'name':cur, 'amount':0, 'totalPrice':0, 'addr':self._addr, 'isDefault':False, 'isShow':False, 'isAddCur':False}
                    lbrTokenEntry = TokenEntry(lbrTokenData)
                    self._tokenModel.appendToken(lbrTokenEntry)
                    self._tokenModelData.append(lbrTokenData)

    def updateVLSCurrencies(self, currencies):
        for cur in currencies:
            if not cur == 'LBR':
                if not self._tokenModel.isExist('violas', cur):
                    vlsTokenData = {'chain':'violas', 'name':cur, 'amount':0, 'totalPrice':0, 'addr':self._addr, 'isDefault':False, 'isShow':False, 'isAddCur':False}
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
    @pyqtSlot(str, str, str, str)
    def sendCoin(self, addr, amount, chain, name):
        amount = int(amount)
        if chain == 'bitcoin':
            pass
        elif chain == 'libra':
            self._libraClient.transfer_coin(self._wallet.accounts[0], 
                    addr, amount, currency_code=name)
        elif chain == 'violas':
            self._client.transfer_coin(self._wallet.accounts[0], 
                    addr, amount, currency_code=name)

    # 二维码
    @pyqtSlot(str, str)
    def genQR(self, chain, name):
        qr = qrcode.QRCode(
                version = 7,
                error_correction = qrcode.constants.ERROR_CORRECT_L,
                box_size = 10,
                border = 4,
                )
        qrURL = 'noknown'
        token = ''
        if chain == 'bitcoin':
            qrURL = 'bitcoin' + ':' + self._bitAddr
            token = 'bitcoin-BTC'
        elif chain == 'libra' or chain == 'violas':
            qrURL = chain + '-' + name + ':' + self._addr
            token = chain + '-' + name
        qr.add_data(qrURL)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        imgFile = 'pypay/qml/icons/qr_{}.png'
        img.save(imgFile.format(token))

    # 交易记录
    @pyqtSlot(dict)
    def history_libra(self, dt):
        data = dt['data']
        for d in data:
            historyEntry = HistoryEntry(d)
            self._historyModel.append(historyEntry)

    @pyqtSlot(dict)
    def history_violas(self, dt):
        data = dt['data']
        for d in data:
            historyEntry = HistoryEntry(d)
            self._historyModel.append(historyEntry)



    @pyqtSlot(str, str, int, int, int)
    def requestVLSHistory(self, addr, currency, flows, offset, limit):
        self._historyModel.clear()
        self.requestViolasHistory.emit({'addr':addr, 'currency':None if currency == '' else currency, 
            'flows':None if flows==-1 else flows, 'offset':offset, 'limit':limit})

    @pyqtSlot(str, str, int, int, int)
    def requestLBRHistory(self, addr, currency, flows, offset, limit):
        self._historyModel.clear()
        self.requestLibraHistory.emit({'addr':addr, 'currency':None if currency == '' else currency, 
            'flows':None if flows==-1 else flows, 'offset':offset, 'limit':limit})

    # 定时器
    def _timeUpdate(self):
        self.requestBitBalance.emit()
        self.requestBitTransactions.emit()
        self.requestLibraCurrencies.emit()
        self.requestViolasCurrencies.emit()
        self.requestLibraBalances.emit()
        self.requestViolasBalances.emit()
        self.requestTotalBalances.emit()

        self.saveToFile()

    # 交易历史
    @pyqtProperty(QObject, constant=True)
    def historyModel(self):
        return self._historyModel

    # 汇率
    @pyqtSlot(dict)
    def updateExchangeRates(self, rates):
        print("rates: ", rates)
        self._rates = rates

    def getRate(self, cur):
        for c, r in self._rates.items():
            if c in cur:
                return r
        return 1

    # 总资产
    @pyqtSlot()
    def updateTotalBalance(self):
        sum = 0
        for data in self._tokenModelData:
            sum += data['totalPrice']
        self._totalBalance = sum
        self.totalBalanceChanged.emit()

    totalBalanceChanged = pyqtSignal()
    @pyqtProperty(float, notify=totalBalanceChanged)
    def totalBalance(self):
        return self._totalBalance
