from violas_client.canoser import Struct
from violas_client.lbrtypes.on_chain_config import OnChainConfig

class RegisteredCurrencies(Struct, OnChainConfig):
    IDENTIFIER = "RegisteredCurrencies"

    _fields = [
        ("currency_codes", [str])
    ]

    def __len__(self):
        return len(self.currency_codes)

    def __getitem__(self, item):
        return self.currency_codes[item]