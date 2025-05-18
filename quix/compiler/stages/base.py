from abc import ABC, abstractmethod

from quix.tools import log


class Stage[I, O](ABC):
    __slots__ = ()

    @log
    def __call__(self, data: I) -> O:
        return self._execute(data)

    @abstractmethod
    def _execute(self, __data: I, /) -> O:
        raise NotImplementedError
