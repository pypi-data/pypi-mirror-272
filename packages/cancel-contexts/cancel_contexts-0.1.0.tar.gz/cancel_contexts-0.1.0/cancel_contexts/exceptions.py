class BaseCancelContextError(Exception):
    pass


class ContextCancelledError(BaseCancelContextError):
    pass
