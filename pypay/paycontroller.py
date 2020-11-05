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
        self._bitKey = None
        self._bitAddr = ''
        self._isImportWallet = False
        self._swap_to_addr = {}
        self._datadir = self.get_datadir() / "pypay"
        self.datadirChanged.emit()
        self._violas_bank_max_borrow_amount = 0
        try:
            self._datadir.mkdir(parents = True)
        except FileExistsError:
            pass

    @pyqtSlot()
    def shutdown(self):
        pass

    def __del__(self):
        if self._bitThread is not None:
            self._bitThread.quit()
            self._bitThread.wait()
        if self._lbrThread is not None:
            self._lbrThread.quit()
            self._lbrThread.wait()
        if self._vlsThread is not None:
            self._vlsThread.quit()
            self._vlsThread.wait()
        del self._client
        del self._libraClient

    requestActiveLibraAccount = pyqtSignal()
    requestActiveViolasAccount = pyqtSignal()
    requestLBRAddCurOfAccount = pyqtSignal(str, bool)
    requestVLSAddCurOfAccount = pyqtSignal(str, bool)
    request_violas_bank_max_borrow_amount = pyqtSignal(str)

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
        self.addr_changed.emit()
        self._libra_addr = self._wallet.accounts[1].address_hex
        self.libra_addr_changed.emit()
        self._mnemonic = self._wallet.mnemonic
        self.mnemonic_changed.emit()

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
        self._bit.moveToThread(self._bitThread)
        self._bitThread.start()

        self._client = Client("violas_testnet")
        #self._client = Client("violas_testnet_out")
        self._libraClient = LibraClient("libra_testnet")

        # libra相关操作
        self._lbrThread = QThread(parent=self)
        self._lbr = Libra(self._libraClient, self._wallet.accounts)
        self._lbrThread.finished.connect(self._lbr.deleteLater)
        self.requestActiveLibraAccount.connect(self._lbr.requestActiveAccount)  # active account
        self.requestLBRAddCurOfAccount.connect(self._lbr.requestAddCurOfAccount)
        self._lbr.moveToThread(self._lbrThread)
        self._lbrThread.start()

        # violas相关操作
        self._vlsThread = QThread(parent=self)
        self._vls = Violas(self._client, self._wallet.accounts)
        self._vlsThread.finished.connect(self._vls.deleteLater)
        self.requestActiveViolasAccount.connect(self._vls.requestActiveAccount) # active account
        self.requestVLSAddCurOfAccount.connect(self._vls.requestAddCurOfAccount)
        self.request_violas_bank_max_borrow_amount.connect(self._vls.get_bank_max_borrow_amount)
        self._vls.get_bank_max_borrow_amount_result.connect(self.get_violas_bank_max_borrow_amount)
        self._vls.moveToThread(self._vlsThread)
        self._vlsThread.start()

        if isFirstCreateWallet:
            self.requestActiveLibraAccount.emit()
            self.requestActiveViolasAccount.emit()

    @pyqtSlot(str)
    def createWalletFromMnemonic(self, mnemonic):
        self._isImportWallet = True
        fileName = self._datadir / "pypay.wallet"
        with open(fileName, 'w') as f:
            f.write(mnemonic + ';2')
        self.createWallet()

    # 助记词
    mnemonic_changed = pyqtSignal()
    @pyqtProperty(str, notify=mnemonic_changed)
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
    addr_changed = pyqtSignal()
    @pyqtProperty(str, notify=addr_changed)
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
        
    # 拷贝
    @pyqtSlot(str)
    def copy(self, str):
        cb = QGuiApplication.clipboard()
        cb.setText(str)

    # 打开网页
    @pyqtSlot(str)
    def openUrl(self, url):
        QDesktopServices.openUrl(QUrl(url))

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

    @pyqtSlot(int)
    def get_violas_bank_max_borrow_amount(self, amount):
        self._violas_bank_max_borrow_amount = amount
        self.violas_bank_max_borrow_amount_changed.emit()

    violas_bank_max_borrow_amount_changed = pyqtSignal()
    @pyqtProperty(int, notify=violas_bank_max_borrow_amount_changed)
    def violas_bank_max_borrow_amount(self):
        return self._violas_bank_max_borrow_amount
