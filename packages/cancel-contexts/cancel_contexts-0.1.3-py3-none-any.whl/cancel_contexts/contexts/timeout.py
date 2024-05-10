import time

from cancel_contexts.contexts.base import BaseContext
from cancel_contexts.exceptions import ContextTimeOutError


class TimeOutContext(BaseContext):
    exception = ContextTimeOutError

    def __init__(self, timeout: float) -> None:
        self.start_time = time.perf_counter()
        self.timeout = timeout
        super().__init__()

    def __bool__(self) -> bool:
        if self.is_timer_finished:
            self.cancel()
        return super().__bool__()

    @property
    def is_timer_finished(self) -> bool:
        timer = time.perf_counter()
        return timer >= (self.start_time + self.timeout)

    def cancel(self) -> None:
        with self.lock:
            self.cancelled = True

    def check_cancelled(self, msg: str | None = None) -> None:
        if self.cancelled or self.is_timer_finished:
            msg = msg or "Context was timed out"
            raise self.exception(msg)
