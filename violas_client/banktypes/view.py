from violas_client.json_rpc.views import TransactionView as LibraTransactionView
from violas_client.banktypes.bytecode import get_code_type, CodeType
from violas_client.lbrtypes.bytecode import CodeType as LibraCodeType
from violas_client.banktypes.account_resources import ViolasEvent
from violas_client.banktypes.account_resources import EventPublish, EventRegisterLibraToken, EventMint, EventTransfer,\
    EventUpdatePrice, EventLock, EventRedeem, EventBorrow, EventRepayBorrow, EventLiquidateBorrow, EventUpdateCollateralFactor, \
    EventEnterBank, EventExitBank, EventUpdateRateModel, EventUpdatePriceFromOracle, EventClaimIncentive, EventSetIncentiveRate

WITH_AMOUNT_TYPE = [CodeType.BORROW, CodeType.ENTER_BANK, CodeType.EXIT_BANK, CodeType.LIQUIDATE_BORROW, CodeType.LOCK,
                    CodeType.REDEEM, CodeType.REPAY_BORROW]

class TransactionView(LibraTransactionView):
    bank_type_maps = {
        CodeType.BORROW2: EventBorrow,
        CodeType.BORROW_INDEX: EventBorrow,
        CodeType.BORROW: EventBorrow,
        CodeType.CREATE_TOKEN: EventRegisterLibraToken,
        CodeType.ENTER_BANK: EventEnterBank,
        CodeType.EXIT_BANK: EventExitBank,
        CodeType.LIQUIDATE_BORROW_INDEX: EventLiquidateBorrow,
        CodeType.LIQUIDATE_BORROW: EventLiquidateBorrow,
        CodeType.LOCK2: EventLock,
        CodeType.LOCK_INDEX: EventLock,
        CodeType.LOCK: EventLock,
        CodeType.MINT: EventMint,
        CodeType.PUBLISH: EventPublish,
        CodeType.REDEEM2: EventRedeem,
        CodeType.REDEEM_INDEX: EventRedeem,
        CodeType.REDEEM: EventRedeem,
        CodeType.REGISTER_LIBRA_TOKEN: EventRegisterLibraToken,
        CodeType.REPAY_BORROW2: EventRepayBorrow,
        CodeType.REPAY_BORROW_INDEX: EventRepayBorrow,
        CodeType.REPAY_BORROW: EventRepayBorrow,
        CodeType.UPDATE_COLLATERAL_FACTOR: EventUpdateCollateralFactor,
        CodeType.UPDATE_PRICE_FROM_ORACLE: EventUpdatePriceFromOracle,
        CodeType.UPDATE_PRICE_INDEX: EventUpdatePrice,
        CodeType.UPDATE_PRICE: EventUpdatePrice,
        CodeType.UPDATE_RATE_MODEL: EventUpdateRateModel,
        CodeType.SET_INCENTIVE_RATE: EventSetIncentiveRate,
        CodeType.CLAIM_INCENTIVE: EventClaimIncentive,
    }

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

    def get_bank_type_events(self, t):
        ret = []
        event_type = self.bank_type_maps.get(t)
        for event in self.get_bank_events():
            if isinstance(event.get_bank_event(), event_type):
                ret.append(event)
        return ret

    def get_amount(self):
        amount = super().get_amount()
        if amount is not None:
            return amount
        type = self.get_code_type()
        if type is not None:
            events = self.get_bank_type_events(type)
            if len(events):
                return events[0].get_amount()

    def get_receiver(self):
        receiver = super().get_receiver()
        if receiver is not None:
            return receiver
        type = self.get_code_type()
        if type is not None:
            events = self.get_bank_type_events(type)
            if len(events):
                return events[0].get_borrower()

    def get_currency_code(self):
        currency_code = super().get_currency_code()
        if currency_code is not None:
            return currency_code
        type = self.get_code_type()
        if type is not None:
            events = self.get_bank_type_events(type)
            if len(events):
                return events[0].get_currency_code()

    def get_collateral_currency(self):
        type = self.get_code_type()
        if type is not None:
            events = self.get_bank_type_events(type)
            if len(events):
                return events[0].get_collateral_currency()

    def get_collateral_amount(self):
        type = self.get_code_type()
        if type is not None:
            events = self.get_bank_type_events(type)
            if len(events):
                return events[0].get_collateral_amount()

    def get_data(self):
        data = super().get_data()
        if data is None:
            type = self.get_code_type()
            if type is not None:
                events = self.get_bank_type_events(type)
                if len(events):
                    return events[0].get_data()
        return data

    def get_price(self):
        type = self.get_code_type()
        events = self.get_bank_type_events(type)
        if len(events):
            return events[0].get_price()

    def get_borrower(self):
        type = self.get_code_type()
        if type == CodeType.LIQUIDATE_BORROW:
            events = self.get_bank_type_events(type)
            if len(events):
                return events[0].get_borrower()

    def get_bank_timestamp(self):
        events = self.get_bank_events()
        if len(events):
            return events[0].get_timestamp()

    def get_incentive(self):
        type = self.get_code_type()
        events = self.get_bank_type_events(type)
        if len(events):
            return events[0].get_incentive()
