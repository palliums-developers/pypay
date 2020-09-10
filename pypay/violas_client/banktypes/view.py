from violas_client.json_rpc.views import TransactionView as LibraTransactionView
from violas_client.banktypes.bytecode import get_code_type, CodeType
from violas_client.lbrtypes.bytecode import CodeType as LibraCodeType
from violas_client.banktypes.account_resources import ViolasEvent

WITH_AMOUNT_TYPE = [CodeType.BORROW, CodeType.ENTER_BANK, CodeType.EXIT_BANK, CodeType.LIQUIDATE_BORROW, CodeType.LOCK,
                    CodeType.REDEEM, CodeType.REPAY_BORROW]


class TransactionView(LibraTransactionView):
    @classmethod
    def new(cls, tx):
        ret = tx
        ret.__class__ = TransactionView
        return ret

    def get_code_type(self):
        type = super().get_code_type()
        if type == LibraCodeType.UNKNOWN:
            return get_code_type(self.get_script_hash())
        return type

    def get_bank_events(self):
        code_type = self.get_code_type()
        events = []
        if code_type in CodeType:
            for event in self.get_events():
                if event.data.enum_name == "Unknown":
                    try:
                        events.append(ViolasEvent.deserialize(bytes.fromhex(event.data.value.raw)))
                    except:
                        pass
        return events

    def get_amount(self):
        amount = super().get_amount()
        if amount is not None:
            return amount
        events = self.get_bank_events()
        if len(events):
            return events[0].get_amount()

    def get_currency_code(self):
        currency_code = super().get_currency_code()
        if currency_code is not None:
            return currency_code
        events = self.get_bank_events()
        if len(events):
            return events[0].get_currency_code()

    def get_data(self):
        data = super().get_data()
        if data is None:
            events = self.get_bank_events()
            for event in events:
                data = event.get_data()
                if data is not None:
                    return data
        return data











