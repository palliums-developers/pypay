from libra_client.lbrtypes.error import LibraError
from libra_client.lbrtypes.vm_error import StatusCode

def ensure(code, msg):
    if not code:
        raise LibraError(StatusCode.ENSURE_ERROR, msg)