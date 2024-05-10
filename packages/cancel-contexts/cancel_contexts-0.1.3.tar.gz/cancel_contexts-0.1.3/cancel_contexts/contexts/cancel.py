from cancel_contexts.contexts.base import BaseContext
from cancel_contexts.exceptions import ContextCancelledError


class CancelContext(BaseContext):
    exception = ContextCancelledError

    def cancel(self) -> None:
        with self.lock:
            self.cancelled = True

    def check_cancelled(self, msg: str | None = None) -> None:
        if self.cancelled:
            msg = msg or "Context was cancelled"
            raise self.exception(msg)
