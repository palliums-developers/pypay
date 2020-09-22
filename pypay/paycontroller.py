import os
import random
import sys
import pickle
import threading
import qrcode
import qrcode.image
import logging
import pathlib
import json

from mnemonic import Mnemonic
from bip32utils import BIP32Key
from bit import PrivateKeyTestnet, wif_to_key

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty, QUrl, QThread, QTimer
from PyQt5.QtGui import QClipboard, QGuiApplication, QDesktopServices

from violas_client import Wallet, Client
from libra_client import Client as LibraClient
from pypay.bitcoin import Bit
from pypay.tokenmodel import TokenEntry, TokenModel
from pypay.depositmodel import DepositEntry, DepositModel
from pypay.depositinfo import DepositInfo
from pypay.borrowinfo import BorrowInfo
from pypay.borrowmodel import BorrowEntry, BorrowModel
from pypay.borrowordermodel import BorrowOrderEntry, BorrowOrderModel
from pypay.tokentypemodel import TokenTypeModel
from pypay.bittransactionmodel import BitTransactionEntry, BitTransactionModel
from pypay.libra import Libra
from pypay.violas import Violas
from pypay.addrbookmodel import AddrBookEntry, AddrBookModel
from pypay.historymodel import HistoryEntry, HistoryModel


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
        self._libra_addr = ''
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
        self._curBalance = 0
        self._datadir = self.get_datadir() / "pypay"
        self._swap_to_addr = {}
        self._deposit = 0
        self._borrow = 0
        self._income = 0
        self._lastdayincome = 0
        self._depositModel = DepositModel()
        self._borrowModel = BorrowModel()
        self._deposit_info = DepositInfo()  # 存款
        self._borrow_info = BorrowInfo()
        self._borrow_order_model = BorrowOrderModel()
        self.datadirChanged.emit()
        try:
            self._datadir.mkdir(parents = True)
        except FileExistsError:
            pass

    @pyqtSlot()
    def shutdown(self):
        self._timer.stop()
        self.saveToFile()
        del self._client
        del self._libraClient

    def __del__(self):
        if self._walletIsCreated == True:
            #self._bitThread.quit()
            self._bitThread.terminate()
            self._bitThread.wait()

            #self._lbrThread.quit()
            self._lbrThread.terminate()
            self._lbrThread.wait()

            #self._vlsThread.quit()
            self._vlsThread.terminate()
            self._vlsThread.wait()

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
    requestBankAccountInfo = pyqtSignal(dict)
    requestBankProductDeposit = pyqtSignal()
    signal_request_deposit_info = pyqtSignal()
    requested_get_bank_product_borrow = pyqtSignal()
    requested_get_bank_borrow_info = pyqtSignal()
    requested_get_bank_borrow_orders = pyqtSignal(dict)

    # 钱包
    @pyqtSlot()

    def createWallet(self):
        fileName = self._datadir / "pypay.wallet"
        isFirstCreateWallet = True
        if os.path.exists(fileName):
            self._wallet = Wallet.recover(fileName)
            isFirstCreateWallet = False
        else:
            self._wallet = Wallet.new()
            account = self._wallet.new_account()
            account1 = self._wallet.new_account()
        self._addr = self._wallet.accounts[0].address_hex
        self.addrChanged.emit()
        self._libra_addr = self._wallet.accounts[1].address_hex
        self.libra_addr_changed.emit()
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

        self._bitThread = QThread(parent=self)
        self._bit = Bit(self._bitKey)
        self._bitThread.finished.connect(self._bit.deleteLater)
        self.requestBitBalance.connect(self._bit.requestBalance)
        self._bit.balanceChanged.connect(self.updateBitBalance)
        self.requestBitTransactions.connect(self._bit.requestTransactions)
        self._bit.transactionsChanged.connect(self.updateBitTransactions)
        self._bit.moveToThread(self._bitThread)
        self._bitThread.start()

        self._client = Client("violas_testnet")
        #self._client = Client("violas_testnet_out")
        self._libraClient = LibraClient("libra_testnet")
        if isFirstCreateWallet or self._isImportWallet:
            # 默认币种列表: BTC, LBR, VLS
            self.setDefaultTokens()

        else:
            self.loadFromFile()

        # libra相关操作
        self._lbrThread = QThread(parent=self)
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
        self._vlsThread = QThread(parent=self)
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
        self._vls.bankAccountInfoChanged.connect(self.update_bank_account_info) # bank account info
        self.requestBankAccountInfo.connect(self._vls.request_bank_account_info)
        self._vls.bankProductDepositChanged.connect(self.update_bank_product_deposit) # bank product deposit
        self.requestBankProductDeposit.connect(self._vls.request_bank_product_deposit)
        self._vls.bank_deposit_infoChanged.connect(self.update_bank_deposit_info) # bank deposit info
        self.signal_request_deposit_info.connect(self._vls.request_bank_deposit_info)
        self._vls.get_bank_product_borrow_result.connect(self.get_bank_product_borrow_result) # bank product borrow
        self.requested_get_bank_product_borrow.connect(self._vls.get_bank_product_borrow)
        self._vls.get_bank_borrow_info_result.connect(self.get_bank_borrow_info_result) # bank borrow info
        self.requested_get_bank_borrow_info.connect(self._vls.get_bank_borrow_info)
        self._vls.get_bank_borrow_orders_result.connect(self.get_bank_borrow_orders_result) # bank borrow orders
        #self.requested_get_borrow_orders.connect(self._vls.get_bank_borrow_orders)
        self._vls.moveToThread(self._vlsThread)
        self._vlsThread.start()

        if isFirstCreateWallet:
            self.requestActiveLibraAccount.emit()
            self.requestActiveViolasAccount.emit()

        self._walletIsCreated = True

        self.requestTotalBalances.connect(self.updateTotalBalance)
        self._timer.timeout.connect(self._timeUpdate)
        #self._timer.start(10000)
        #self._timeUpdate()

        #self.requestExchangeRates.emit()
        #self.request_bank_product_deposit()

        # TODO https://api .violas.io//1.0/market/exchange/crosschain/address/info

    @pyqtSlot(str)
    def createWalletFromMnemonic(self, mnemonic):
        self._isImportWallet = True
        fileName = self._datadir / "pypay.wallet"
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

    # libra地址
    libra_addr_changed = pyqtSignal()
    @pyqtProperty(str, notify=libra_addr_changed)
    def libra_addr(self):
        return self._libra_addr

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
            totalPrice = round(amount * rate, 2)
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
            totalPrice = round(amount * rate, 2)
            print("rate: ", rate)
            self._tokenModel.changeData({'chain':'violas', 'name':key, 'amount':amount, 'totalPrice':totalPrice})
            for data in self._tokenModelData:
                if data['chain'] == 'violas' and data['name'] == key:
                    data['amount'] = amount
                    data['totalPrice'] = totalPrice

    # tokenmodel 保存，恢复
    def loadFromFile(self):
        filename = self._datadir / 'pypay.tokenmodel'
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                self._tokenModelData = pickle.load(f)
                for d in self._tokenModelData:
                    entry = TokenEntry(d)
                    self._tokenModel.appendToken(entry)
        filename = self._datadir / 'pypay.addrbookmodel'
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                self._addrBookModelData = pickle.load(f)
                for d in self._addrBookModelData:
                    entry = AddrBookEntry(d)
                    self._addrBookModel.append(entry)

        self.updateTotalBalance()

    def saveToFile(self):
        filename = self._datadir / 'pypay.tokenmodel'
        with open(filename, 'wb') as f:
            pickle.dump(self._tokenModelData, f)
        filename = self._datadir / 'pypay.addrbookmodel'
        with open(filename, 'wb') as f:
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
        amount = float(amount)
        if chain == 'bitcoin':
            amount = int(amount * 1_0000_0000)
            pass
        elif chain == 'libra':
            amount = int(amount * 1_000_000)
            self._libraClient.transfer_coin(self._wallet.accounts[0], 
                    addr, amount, currency_code=name)
        elif chain == 'violas':
            amount = int(amount * 1_000_000)
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
        imgFile = str(self._datadir) + '/qr_{}.png'
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

        self.requestBankAccountInfo.emit({'address':self._addr})

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
        return 0

    # 总资产
    @pyqtSlot()
    def updateTotalBalance(self):
        sum = 0
        for data in self._tokenModelData:
            #print("totalBalance: ", data['totalPrice'])
            sum += data['totalPrice']
        self._totalBalance = round(sum, 2)
        self.totalBalanceChanged.emit()

    totalBalanceChanged = pyqtSignal()
    @pyqtProperty(float, notify=totalBalanceChanged)
    def totalBalance(self):
        return self._totalBalance

    # 币种余额
    @pyqtSlot(str, str)
    def getCurBalance(self, chain, name):
        for data in self._tokenModelData:
            if data['chain'] == chain and data['name'] == name:
                print("getCurBalance: ", data['amount'])
                self._curBalance = data['amount']
        self.curBalanceChanged.emit()

    curBalanceChanged = pyqtSignal()
    @pyqtProperty(float, notify=curBalanceChanged)
    def curBalance(self):
        return self._curBalance

    def get_datadir(self) -> pathlib.Path:
        """
        Returns a parent directory path
        where persistent application data can be stored.

        # linux: ~/.local/share
        # macOS: ~/Library/Application Support
        # windows: C:/Users/<USER>/AppData/Roaming
        """

        home = pathlib.Path.home()

        if sys.platform == "win32":
            return home / "AppData/Roaming"
        elif sys.platform == "linux":
            return home / ".local/share"
        elif sys.platform == "darwin":
            return home / "Library/Application Support"

    datadirChanged = pyqtSignal()
    @pyqtProperty(str, notify=datadirChanged)
    def datadir(self):
        return str(self._datadir)


    @pyqtSlot(str, str, float, str, str, float)
    def swap_from_violas_or_libra(self, chain_name_in, coin_name_in, coin_amount_in, chain_name_out, coin_name_out, coin_amount_out):
        flag = ''
        type = ''
        to_addr = ''
        to_addr2 = ''

        if chain_name_in == 'libra' and chain_name_out == 'violas':
            flag = 'libra'
            if coin_name_out == 'VLSUSD':
                type = 'l2vusd'
            elif coin_name_out == 'VLSGBP':
                type = 'l2vgbp'
            elif coin_name_out == 'VLSEUR':
                type = 'l2veur'
            elif coin_name_out == 'VLSJPY':
                type = 'l2vjpy'
            elif coin_name_out == 'VLSSGD':
                type = 'l2vsgd'
            to_addr = self._swap_to_addr[type]
            to_addr2 = "00000000000000000000000000000000" + self._swap_to_addr[type]

        elif chain_name_in == 'libra' and chain_name_out == 'bitcoin':
            flag = 'libra'
            type = 'l2b'
            to_addr = self._swap_to_addr[type]
            to_addr2 = self._swap_to_addr[type]

        elif chain_name_in == 'violas' and chain_name_out == 'libra':
            flag = 'violas'
            if coin_name_out == 'Coin1':
                type = 'v2lusd'
            elif coin_name_out == 'Coin2':
                type = 'v2leur'
            to_addr = self._swap_to_addr[type]
            to_addr2 = "00000000000000000000000000000000" + self._swap_to_addr[type]

        elif chain_name_in == 'violas' and chain_name_out == 'bitcoin':
            flag = 'violas'
            type = 'v2b'
            to_addr = self._swap_to_addr[type]
            to_addr2 = self._swap_to_addr[type]

        print("flag: ", flag, "type: ", type, "to_address: ", to_addr)
        payload = {"flag": flag, "type": type, "to_address": to_address2, "state":"start", "out_amount":coin_amount_out * 1_000_000, "times":0}

        if chain_name_in == 'libra':
            self._libraClient.transfer_coin(self._wallet.accounts[0], 
                    to_addr, coin_amount_in * 1_000_000, currency_code=coin_name_in, data=json.dumps(payload))
        elif chain_name_in == 'violas':
            self._client.transfer_coin(self._wallet.accounts[0], 
                    to_addr, coin_amount_in * 1_000_000, currency_code=coin_name_in, data=json.dumps(payload))


    @pyqtSlot(float, str, str, float)
    def swap_from_bitcoin(self, coin_amount_in, chain_name_out, coin_name_out, coin_amount_out):
        pass
        #mark = 0x76696f6c6173
        #version = 0x0003

        #type = 
        #if chain_name_out == 'violas':
        #    if coin_name_out == 'VLSUSD':

    # 存款总额
    depositChanged = pyqtSignal()
    @pyqtProperty(float, notify=depositChanged)
    def deposit(self):
        return self._deposit

    # 可借总额
    borrowChanged = pyqtSignal()
    @pyqtProperty(float, notify=borrowChanged)
    def borrow(self):
        return self._borrow

    # 累计收益
    incomeChanged = pyqtSignal()
    @pyqtProperty(float, notify=incomeChanged)
    def income(self):
        return self._income

    # 昨日收益
    lastdayincomeChanged = pyqtSignal()
    @pyqtProperty(float, notify=lastdayincomeChanged)
    def lastdayincome(self):
        return self._lastdayincome

    # 存款
    @pyqtProperty(QObject, constant=True)
    def depositModel(self):
        return self._depositModel

    # 借款
    @pyqtProperty(QObject, constant=True)
    def borrowModel(self):
        return self._borrowModel

    # 更新银行账户信息
    @pyqtSlot(dict)
    def update_bank_account_info(self, info):
        data = info['data']
        self._deposit = data['amount']
        self.depositChanged.emit()
        self._borrow = data['borrow']
        self.borrowChanged.emit()
        self._income = data['total']
        self.incomeChanged.emit()
        self._lastdayincome = data['yesterday']
        self.lastdayincomeChanged.emit()

    # 更新存款产品列表
    @pyqtSlot(dict)
    def update_bank_product_deposit(self, dt):
        print(dt)
        data = dt['data']

        ## TEST
        #dt1 = {'desc':"hello", 'id':'1', 'logo':'', 'name':'name', 'rate':0.1, 'rate_desc':'年利率', 'token_module':'BTC'}
        #dt2 = {'desc':"hello2", 'id':'2', 'logo':'', 'name':'name2', 'rate':0.2, 'rate_desc':'年利率', 'token_module':'BTC'}
        #data = []
        #data.append(dt1)
        #data.append(dt2)

        for d in data:
            depositEntry = DepositEntry(d)
            self._depositModel.append(depositEntry)

    # 请求存款产品列表
    @pyqtSlot()
    def request_bank_product_deposit(self):
        print("request_bank_product_deposit")
        self._depositModel.clear()
        self.requestBankProductDeposit.emit()

    # 获取存款产品信息
    @pyqtSlot(str)
    def request_bank_deposit_info(self, id):
        self._deposit_info.clear()
        self.signal_request_deposit_info.emit()

    @pyqtSlot(dict)
    def update_bank_deposit_info(self, dt):
        data = dt['data']
        self._deposit_info = DepositInfo(data)

    # 获取存款订单信息
    # /1.0/violas/bank/deposit/orders

    #获取存款订单列表
    # /1.0/violas/bank/deposit/order/list

    # 获取借贷产品列表
    @pyqtSlot()
    def get_bank_product_borrow(self):
        self._borrowModel.clear()
        self.requested_get_bank_product_borrow.emit()

    @pyqtSlot(dict)
    def get_bank_product_borrow_result(self, dt):
        data = dt['data']
        for d in data:
            borrowEntry = BorrowEntry(d)
            self._borrowModel.append(borrowEntry)

    # 获取借贷产品信息
    @pyqtSlot()
    def get_bank_borrow_info(self):
        self._borrow_info.clear()
        self.requested_get_bank_borrow_info.emit()

    @pyqtSlot(dict)
    def get_bank_borrow_info_result(self, dt):
        data = dt['data']
        self._borrow_info = BorrowInfo(data)

    # 获取借贷订单信息
    @pyqtSlot(str, int, int)
    def get_bank_borrow_orders(self, address, offset, limit):
        self._borrow_orders_model.clear()
        self.requested_get_bank_borrow_orders.emit({'address':address, 'offset':offset, 'limit':limit})

    @pyqtSlot(dict)
    def get_bank_borrow_orders_result(self, dt):
        data = dt['data']
        for d in data:
            borrow_order_entry = BorrowOrderEntry(d)
            self._borrow_order_model.append(borrow_order_entry)

    # 获取借贷订单列表
    # /1.0/violas/bank/borrow/order/list
    @pyqtSlot(str, str, int, int, int)
    def get_bank_borrow_order_list(self, address, currency, status, offset, limit):
        self._borrow_order_list_model.clear()
        self.requested_get_bank_borrow_order_list.emit({'address':address, 'currency':currency, 'status':status, 'offset':offset, 'limit':limit})

    # 获取借贷订单详情
    # /1.0/violas/bank/borrow/order/detail
    @pyqtSlot(str, str, int, int, int)
    def get_bank_borrow_order_detail(self, address, id, q, offset, limit):
        self._borrow_order_detail.clear()
        self.requested_get_bank_borrow_order_detail.emit({'address':address, 'id':id, 'q':q, 'offset':offset, 'limit':limit})

    # 存款提取
    # /1.0/violas/bank/deposit/withdrawal

    # 借贷还款
    # /1.0/violas/bank/borrow/repayment
