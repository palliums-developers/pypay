from violas_client.extypes.view import TransactionView as ExchangeTransactionView
from violas_client.banktypes.view import TransactionView as BankTransactionView
from violas_client.oracle_client.view import TransactionView as OracleTransactionView
from violas_client.lbrtypes.bytecode import CodeType as LibraCodeType

class TransactionView(ExchangeTransactionView, BankTransactionView, OracleTransactionView):

    @classmethod
    def new(cls, tx):
        ret = super().new(tx)
        ret.__class__ = cls
        return ret

    def get_code_type(self):
        type = ExchangeTransactionView.get_code_type(self)
        if type == LibraCodeType.UNKNOWN:
            return BankTransactionView.get_code_type(self)
        return type

    def get_amount(self):
        return BankTransactionView.get_amount(self)