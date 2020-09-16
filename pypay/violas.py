from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject
from violas_client import Wallet, Client
import requests

class Violas(QObject):
    def __init__(self, client, accounts, parent=None):
        QObject.__init__(self, parent)
        self._client = client
        self._accounts = accounts

    # mint

    @pyqtSlot()
    def requestActiveAccount(self):
        try:
            self._client.mint_coin(self._accounts[0].address, 500_000,
                    auth_key_prefix=self._accounts[0].auth_key_prefix, currency_code="LBR")
        except Exception as result:
            print(result)

    # currencies

    currenciesChanged = pyqtSignal(list)

    @pyqtSlot()
    def requestCurrencies(self):
        try:
            currencies = self._client.get_registered_currencies()
            self.currenciesChanged.emit(currencies)
        except Exception as result:
            print(result)

    # balances

    balancesChanged = pyqtSignal(dict)

    @pyqtSlot()
    def requestBalances(self):
        try:
            balances = self._client.get_balances(self._accounts[0].address_hex)
            self.balancesChanged.emit(balances)

        except Exception as result:
            print(result)

    # history

    historyChanged = pyqtSignal(dict)

    @pyqtSlot(dict)
    def requestHistory(self, dt):
        r = requests.get('https://api4.violas.io/1.0/violas/transaction', params=dt)
        print(r.url)
        if r.status_code == 200:
            self.historyChanged.emit(r.json())
        else:
            print("request error")

    # add cur of account
    @pyqtSlot(str, bool)
    def requestAddCurOfAccount(self, cur, isShow):
        if isShow:
            try:
                self._client.add_currency_to_account(self._accounts[0], cur)
            except Exception as result:
                print(result)
        else:
            pass

    # exchange rates
    
    exchangeRatesChanged = pyqtSignal(dict)

    @pyqtSlot()
    def requestExchangeRates(self):
        r = requests.get('https://api.exchangeratesapi.io/latest?base=USD')
        rates = r.json()['rates']
        self.exchangeRatesChanged.emit(rates)

    # bank account info

    bankAccountInfoChanged = pyqtSignal(dict)

    @pyqtSlot(dict)
    def request_bank_account_info(self, dt):
        r = requests.get('https://api4.violas.io/1.0/violas/bank/account/info', params=dt)
        print(r.url)
        if r.status_code == 200:
            self.bankAccountInfoChanged.emit(r.json())
        else:
            print("request error")


    # bank product deposit

    bankProductDepositChanged = pyqtSignal(dict)

    @pyqtSlot()
    def request_bank_product_deposit(self):
        r = requests.get('https://api4.violas.io/1.0/violas/bank/product/deposit')
        print(r.url)
        if r.status_code == 200:
            self.bankProductDepositChanged.emit(r.json())
        else:
            print("request error")

    # bank deposit info
    bank_deposit_infoChanged = pyqtSignal(dict)

    @pyqtSlot()
    def request_bank_deposit_info(self):
        r = requests.get('https://api4.violas.io/1.0/violas/bank/deposit/info')
        print(r.url)
        if r.status_code == 200:
            self.bank_deposit_infoChanged.emit(r.json())
        else:
            print("request error")


    get_bank_product_borrow_result = pyqtSignal(dict)

    @pyqtSlot()
    def get_bank_product_borrow(self):
        r = requests.get('https://api4.violas.io/1.0/violas/bank/product/borrow')
        print(r.url)
        if r.status_code == 200:
            self.get_bank_product_borrow_result.emit(r.json())
        else:
            print("request error")

    get_bank_borrow_info_result = pyqtSignal(dict)

    @pyqtSlot()
    def get_bank_borrow_info(self):
        r = requests.get('https://api4.violas.io/1.0/violas/bank/borrow/info')
        print(r.url)
        if r.status_code == 200:
            self.get_bank_borrow_info_result.emit(r.json())
        else:
            print("request error")
