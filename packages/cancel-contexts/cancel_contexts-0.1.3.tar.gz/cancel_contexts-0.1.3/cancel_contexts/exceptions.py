class BaseCancelContextError(Exception):
    pass


class ContextCancelledError(BaseCancelContextError):
    pass


class ContextTimeOutError(BaseCancelContextError):
    pass
