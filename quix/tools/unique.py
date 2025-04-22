from threading import Lock
from typing import Final, final

from .singleton import SingletonMeta


@final
class _Counter(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._lock = Lock()
        self._counter = 0

    def step(self) -> int:
        with self._lock:
            self._counter += 1
            return self._counter


_COUNTER: Final[_Counter] = _Counter()


def generate_unique_id() -> int:
    return _COUNTER.step()
