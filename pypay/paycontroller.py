import os
import random
import sys
import pickle
import threading
import qrcode
import qrcode.image
import logging
import pathlib
import shutil
import json

from mnemonic import Mnemonic
from bip32utils import BIP32Key
from bit import PrivateKeyTestnet, wif_to_key

from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot, QUrl, QThread, QTimer, QCoreApplication, QTranslator, QLocale
from PyQt5.QtGui import QClipboard, QGuiApplication, QDesktopServices
from PyQt5.QtQml import QQmlApplicationEngine

from violas_client import Wallet, Client
from libra_client import Client as LibraClient

from pypay.libra import Libra
from pypay.violas import Violas


class PayController(QObject):
    def __init__(self, parent = None, engine = None, app_path = None):
        super().__init__(parent)
        self._engine = engine
        self._app_path = app_path
        self._system_locale_name = QLocale().name()
        print(self._system_locale_name)
        self._lbrThread = QThread(parent=self)
        self._vlsThread = QThread(parent=self)
        self._wallet = None
        self._client = None
        self._libraClient = None
        self._mnemonic = ''
        self._mnemonic_random = ''
        self._mnemonicConfirm = ''
        self._isConfirming = False
        self._key_prefix_hex_violas = ''
        self._address_violas = ''
        self._key_prefix_hex_libra = ''
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

    changed_mnemonic = pyqtSignal()
    @pyqtProperty(str, notify=changed_mnemonic)
    def mnemonic(self):
        return self._mnemonic

    changed_mnemonic_random = pyqtSignal()
    @pyqtProperty(str, notify=changed_mnemonic_random)
    def mnemonic_random(self):
        return self._mnemonic_random

    request_violas_bank_max_borrow_amount = pyqtSignal(str)

    # 钱包
    @pyqtSlot()
    def create_wallet(self):
        fileName = self._data_dir / "pypay.wallet"
        if os.path.exists(fileName):
            self._wallet = Wallet.recover(fileName)
        else:
            self._wallet = Wallet.new()
            account = self._wallet.new_account()
            account1 = self._wallet.new_account()
        self._key_prefix_hex_violas =  self._wallet.accounts[0].auth_key_prefix.hex()
        self._address_violas = self._wallet.accounts[0].address_hex
        self.changed_address_violas.emit()
        self._key_prefix_hex_libra =  self._wallet.accounts[1].auth_key_prefix.hex()
        self._address_libra = self._wallet.accounts[1].address_hex
        self.changed_address_libra.emit()
        self._mnemonic = self._wallet.mnemonic
        self.changed_mnemonic.emit()

        # bitcoin testnet
        mnemo = Mnemonic("english")
        entropy = mnemo.to_entropy(self._mnemonic)
        m = BIP32Key.fromEntropy(entropy, False, True)
        wif = m.WalletImportFormat()
        self._bitKey = wif_to_key(wif)
        self._address_bitcoin = self._bitKey.segwit_address
        self.changed_address_bitcoin.emit()

        self._wallet.write_recovery(fileName)

        self._client = Client.new("http://13.68.141.242:50001")
        self._libraClient = LibraClient("diem_testnet")

        # libra相关操作
        self._lbr = Libra(self._libraClient, self._wallet.accounts)
        self._lbrThread.finished.connect(self._lbr.deleteLater)
        self._lbr.moveToThread(self._lbrThread)
        self._lbrThread.start()

        # violas相关操作
        self._vls = Violas(self._client, self._wallet.accounts)
        self._vlsThread.finished.connect(self._vls.deleteLater)
        self.request_violas_add_currency.connect(self._vls.add_currency)
        self.request_violas_bank_max_borrow_amount.connect(self._vls.get_bank_max_borrow_amount)
        self._vls.get_bank_max_borrow_amount_result.connect(self.get_violas_bank_max_borrow_amount)
        self._vls.moveToThread(self._vlsThread)
        self._vlsThread.start()

    @pyqtSlot(str)
    def create_wallet_from_mnemonic(self, mnemonic):
        self._isImportWallet = True
        fileName = self._data_dir / "pypay.wallet"
        with open(fileName, 'w') as f:
            f.write(mnemonic + ';2')
        self.create_wallet()

    # 删除钱包
    @pyqtSlot()
    def delete_wallet(self):
        try:
            shutil.rmtree(self._data_dir)
        except FileExistsError:
            pass

    @pyqtSlot()
    def gen_random_mnemonic(self):
        self._mnemonic_random = ''
        mneList = self._wallet.mnemonic.split(" ")
        random.shuffle(mneList)
        self._mnemonic_random = ' '.join(mneList)
        self.changed_mnemonic_random.emit()

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

    changed_key_prefix_hex_violas = pyqtSignal()
    @pyqtProperty(str, notify=changed_key_prefix_hex_violas)
    def key_prefix_hex_violas(self):
        return self._key_prefix_hex_violas

    # 地址
    changed_address_violas = pyqtSignal()
    @pyqtProperty(str, notify=changed_address_violas)
    def address_violas(self):
        return self._address_violas

    changed_key_prefix_hex_libra = pyqtSignal()
    @pyqtProperty(str, notify=changed_key_prefix_hex_libra)
    def key_prefix_hex_libra(self):
        return self._key_prefix_hex_libra

    # libra地址
    changed_address_libra = pyqtSignal()
    @pyqtProperty(str, notify=changed_address_libra)
    def address_libra(self):
        return self._address_libra

    # btc地址
    changed_address_bitcoin = pyqtSignal()
    @pyqtProperty(str, notify=changed_address_bitcoin)
    def address_bitcoin(self):
        return self._address_bitcoin
        
    # 拷贝
    @pyqtSlot(str)
    def copy_text(self, str):
        cb = QGuiApplication.clipboard()
        cb.setText(str)

    # 打开网页
    @pyqtSlot(str)
    def open_url(self, url):
        QDesktopServices.openUrl(QUrl(url))

    # 发送
    @pyqtSlot(str, str, str, str)
    def send_coin(self, addr, amount, chain, name):
        amount = float(amount)
        if chain == 'bitcoin':
            amount = int(amount * 1_0000_0000)
            pass
        elif chain == 'diem':
            amount = int(amount * 1_000_000)
            self._libraClient.transfer_coin(self._wallet.accounts[0], 
                    addr, amount, currency_code=name)
        elif chain == 'violas':
            amount = int(amount * 1_000_000)
            self._client.transfer_coin(self._wallet.accounts[0], 
                    addr, amount, currency_code=name)

    # 二维码
    @pyqtSlot(str, str)
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
        elif chain == 'diem' or chain == 'violas':
            tmp_addr = self._address_violas if chain == 'violas' else self._address_libra
            qrURL = chain + '://tdm' + tmp_addr + '?c=' + name
            token = chain + '-' + name
        print("qr url: ", qrURL)
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

    changed_data_dir = pyqtSignal()
    @pyqtProperty(str, notify=changed_data_dir)
    def data_dir(self):
        return str(self._data_dir)

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

    request_violas_add_currency = pyqtSignal(str)
    @pyqtSlot(str, str)
    def publish_currency(self, chain, currency):
        if chain == 'violas':
            self.request_violas_add_currency.emit(currency)

    changed_system_locale_name = pyqtSignal()
    @pyqtProperty(str, notify=changed_system_locale_name)
    def system_locale_name(self):
        return str(self._system_locale_name)

    @pyqtSlot(str)
    def change_locale(self, locale_name):
        app = QCoreApplication.instance()
        translator = QTranslator()
        translator.load(self._app_path + '/i18n/' + locale_name + '.qm')
        app.installTranslator(translator)
        self._engine.retranslate()
