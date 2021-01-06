from violas_client.json_rpc.views import TransactionView as LibraTransactionView
from violas_client.oracle_client.bytecodes import get_code_type, CodeType
from violas_client.oracle_client.oracle_resource import UpdateEvent
from violas_client.lbrtypes.bytecode import CodeType as LibraCodeType

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

    def get_oracle_event(self):
        code_type = self.get_code_type()
        try:
            if code_type in CodeType:
                for event in self.get_events():
                    if event.data.enum_name == "Unknown":
                        return UpdateEvent.deserialize(bytes.fromhex(event.data.value.raw))
        except:
            pass

    def get_currency_code(self):
        currency_code = super().get_currency_code()
        if currency_code is not None:
            return currency_code
        event = self.get_oracle_event()
        if event is not None:
            return event.get_currency_code()

    def get_oracle_time(self):
        event = self.get_oracle_event()
        if event is not None:
            return event.get_timestamp()








