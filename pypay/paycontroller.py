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

from PySide6.QtCore import QObject, Property, Signal, Slot, QUrl, QThread, QTimer
from PySide6.QtGui import QClipboard, QGuiApplication, QDesktopServices

from violas_client import Wallet, Client
from libra_client import Client as LibraClient

from pypay.libra import Libra
from pypay.violas import Violas


class PayController(QObject):
    def __init__(self, parent = None):
        super().__init__(parent)
        self._lbrThread = QThread(parent=self)
        self._vlsThread = QThread(parent=self)
        self._wallet = None
        self._client = None
        self._libraClient = None
        self._mnemonic = ''
        self._mnemonic_random = ''
        self._mnemonicConfirm = ''
        self._isConfirming = False
        self._address_violas = ''
        self._address_libra = ''
        self._bitKey = None
        self._address_bitcoin = ''
        self._isImportWallet = False
        self._swap_to_addr = {}
        self._data_dir = self.get_data_dir() / "PyPay"
        self.changed_data_dir.emit()
        self._violas_bank_max_borrow_amount = 0
        try:
            self._data_dir.mkdir(parents = True)
        except FileExistsError:
            pass

    def __del__(self):
        if self._lbrThread is not None:
            self._lbrThread.quit()
            self._lbrThread.wait()
        if self._vlsThread is not None:
            self._vlsThread.quit()
            self._vlsThread.wait()
        del self._client
        del self._libraClient

    changed_mnemonic = Signal()
    @Property(str, notify=changed_mnemonic)
    def mnemonic(self):
        return self._mnemonic

    changed_mnemonic_random = Signal()
    @Property(str, notify=changed_mnemonic_random)
    def mnemonic_random(self):
        return self._mnemonic_random

    requestActiveLibraAccount = Signal()
    requestActiveViolasAccount = Signal()
    requestLBRAddCurOfAccount = Signal(str, bool)
    requestVLSAddCurOfAccount = Signal(str, bool)
    request_violas_bank_max_borrow_amount = Signal(str)

    # 钱包
    @Slot()
    def create_wallet(self):
        fileName = self._data_dir / "pypay.wallet"
        isFirstCreateWallet = True
        if os.path.exists(fileName):
            self._wallet = Wallet.recover(fileName)
            isFirstCreateWallet = False
        else:
            self._wallet = Wallet.new()
            account = self._wallet.new_account()
            account1 = self._wallet.new_account()
        self._address_violas = self._wallet.accounts[0].address_hex
        self.changed_address_violas.emit()
        self._address_libra = self._wallet.accounts[1].address_hex
        self.changed_address_libra.emit()
        self._mnemonic = self._wallet.mnemonic
        self.changed_mnemonic.emit()

        # bitcoin testnet
        #mnemo = Mnemonic("english")
        #entropy = mnemo.to_entropy(self._mnemonic)
        #m = BIP32Key.fromEntropy(entropy, False, True)
        #wif = m.WalletImportFormat()
        #self._bitKey = wif_to_key(wif)
        #self._address_bitcoin = self._bitKey.segwit_address

        self._wallet.write_recovery(fileName)

        self._client = Client.new("http://51.140.241.96:50001")
        self._libraClient = LibraClient("libra_testnet")

        # libra相关操作
        self._lbr = Libra(self._libraClient, self._wallet.accounts)
        self._lbrThread.finished.connect(self._lbr.deleteLater)
        self.requestActiveLibraAccount.connect(self._lbr.requestActiveAccount)  # active account
        self.requestLBRAddCurOfAccount.connect(self._lbr.requestAddCurOfAccount)
        self._lbr.moveToThread(self._lbrThread)
        self._lbrThread.start()

        # violas相关操作
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

    @Slot(str)
    def create_wallet_from_mnemonic(self, mnemonic):
        self._isImportWallet = True
        fileName = self._data_dir / "pypay.wallet"
        with open(fileName, 'w') as f:
            f.write(mnemonic + ';2')
        self.create_wallet()

    @Slot()
    def gen_random_mnemonic(self):
        self._mnemonic_random = ''
        mneList = self._wallet.mnemonic.split(" ")
        random.shuffle(mneList)
        self._mnemonic_random = ' '.join(mneList)
        self.changed_mnemonic_random.emit()

    # 添加要确认的助记词
    @Slot(str)
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
    changed_address_violas = Signal()
    @Property(str, notify=changed_address_violas)
    def address_violas(self):
        return self._address_violas

    # libra地址
    changed_address_libra = Signal()
    @Property(str, notify=changed_address_libra)
    def address_libra(self):
        return self._address_libra

    # btc地址
    changed_address_bitcoin = Signal()
    @Property(str, notify=changed_address_bitcoin)
    def address_bitcoin(self):
        return self._address_bitcoin
        
    # 拷贝
    @Slot(str)
    def copy_text(self, str):
        cb = QGuiApplication.clipboard()
        cb.setText(str)

    # 打开网页
    @Slot(str)
    def open_url(self, url):
        QDesktopServices.openUrl(QUrl(url))

    # 发送
    @Slot(str, str, str, str)
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
    @Slot(str, str)
    def gen_qr(self, chain, name):
        qr = qrcode.QRCode(
                version = 7,
                error_correction = qrcode.constants.ERROR_CORRECT_L,
                box_size = 10,
                border = 4,
                )
        qrURL = 'noknown'
        token = ''
        if chain == 'bitcoin':
            qrURL = 'bitcoin' + ':' + self._address_bitcoin
            token = 'bitcoin-BTC'
        elif chain == 'libra' or chain == 'violas':
            qrURL = chain + '-' + name + ':' + self._addr
            token = chain + '-' + name
        qr.add_data(qrURL)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        imgFile = str(self._data_dir) + '/qr_{}.png'
        img.save(imgFile.format(token))

    def get_data_dir(self) -> pathlib.Path:
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

    changed_data_dir = Signal()
    @Property(str, notify=changed_data_dir)
    def data_dir(self):
        return str(self._data_dir)

    @Slot(str, str, float, str, str, float)
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


    @Slot(float, str, str, float)
    def swap_from_bitcoin(self, coin_amount_in, chain_name_out, coin_name_out, coin_amount_out):
        pass
        #mark = 0x76696f6c6173
        #version = 0x0003

        #type = 
        #if chain_name_out == 'violas':
        #    if coin_name_out == 'VLSUSD':

    @Slot(int)
    def get_violas_bank_max_borrow_amount(self, amount):
        self._violas_bank_max_borrow_amount = amount
        self.violas_bank_max_borrow_amount_changed.emit()

    violas_bank_max_borrow_amount_changed = Signal()
    @Property(int, notify=violas_bank_max_borrow_amount_changed)
    def violas_bank_max_borrow_amount(self):
        return self._violas_bank_max_borrow_amount

    @Slot(str, str)
    def publish_currency(self, chain, currency):
        print("chain: ", chain)
        print("currency: ", currency)
        thread = threading.Thread(target = violas_publish_currency, args=(currency,))
        thread.start()

def violas_publish_currency(*currency):
    for cur in currency:
        print(threading.current_thread().getName() + " " + cur)
