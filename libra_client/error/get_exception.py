from libra_client.error import LibraError

def get_exception(func):
    def catch_execption_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return None
            raise LibraError(message=str(e))
    return catch_execption_func


