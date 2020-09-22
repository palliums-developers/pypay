from violas_client.lbrtypes.transaction.module import Module as LibraModule
from violas_client.move_core_types.account_address import AccountAddress as Address
from violas_client.banktypes.bytecode import get_code, CodeType

class Module(LibraModule):
    @staticmethod
    def gen_module(module_address=None):
        code = get_code(CodeType.BANK, module_address)
        return Module(code)