from violas_client.error.error import LibraError
from violas_client.lbrtypes.vm_error import StatusCode

def ensure(code, msg):
    if not code:
        raise LibraError(StatusCode.ENSURE_ERROR, msg)