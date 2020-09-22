from violas_client.canoser.base import Base
from violas_client.canoser.rust_optional import RustOptional

class Optional(RustOptional):
    _type = None

    @classmethod
    def from_type(cls, type):
        ret = cls
        ret._type = type
        return ret
