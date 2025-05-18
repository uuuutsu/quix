from abc import ABC, abstractmethod


class Stage[I, O](ABC):
    __slots__ = ()

    def __call__(self, data: I) -> O:
        return self._execute(data)

    @abstractmethod
    def _execute(self, __data: I, /) -> O:
        raise NotImplementedError
