from violas_client.lbrtypes.transaction.module import Module as LibraModule
from violas_client.move_core_types.account_address import AccountAddress as Address
from violas_client.extypes.bytecode import get_code, CodeType

class Module(LibraModule):
    @staticmethod
    def gen_module(module_name, module_address):
        module_address = Address.normalize_to_bytes(module_address)
        code = get_code(module_name, module_address)
        return Module(code)