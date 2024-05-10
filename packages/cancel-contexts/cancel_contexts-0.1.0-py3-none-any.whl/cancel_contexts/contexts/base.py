from threading import RLock
from typing import Any, ParamSpec, Self

from cancel_contexts.exceptions import BaseCancelContextError

P = ParamSpec("P")


class BaseContext:
    exception = BaseCancelContextError

    def __init__(self, *args: P.args, **kwargs: P.kwargs) -> None:
        self.__cancelled = False
        self.lock = RLock()

    def __enter__(self) -> Self:
        return self

    def __bool__(self) -> bool:
        return not self.cancelled

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        with self.lock:
            self.__cancelled = True

    @property
    def cancelled(self) -> bool:
        with self.lock:
            return self.__cancelled

    @cancelled.setter
    def cancelled(self, value: bool) -> None:
        with self.lock:
            if self.__cancelled:
                msg = "Context already cancelled"
                raise self.exception(msg)

            self.__cancelled = value

    def check_cancelled(self, msg: str | None = None) -> None:
        if self.cancelled:
            msg = msg or "Context was cancelled"
            raise self.exception(msg)

    def cancel(self) -> None:
        raise NotImplementedError
