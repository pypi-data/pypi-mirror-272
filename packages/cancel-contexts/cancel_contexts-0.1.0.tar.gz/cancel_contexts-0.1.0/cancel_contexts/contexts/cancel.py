from cancel_contexts.contexts.base import BaseContext
from cancel_contexts.exceptions import ContextCancelledError


class CancelContext(BaseContext):
    exception = ContextCancelledError

    def cancel(self) -> None:
        with self.lock:
            self.cancelled = True
