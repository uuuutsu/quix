from __future__ import annotations

from dataclasses import dataclass

from .base import Stage


@dataclass(slots=True)
class Composite[I, T, O](Stage[I, O]):
    left: Stage[I, T]
    right: Stage[T, O]

    def __call__(self, data: I) -> O:
        return self._execute(data)

    def _execute(self, __data: I) -> O:
        return self.right(self.left(__data))


@dataclass(slots=True)
class Pipe[I, O](Stage[I, O]):
    curr: Stage[I, O]

    def __or__[NewO](self, next: Stage[O, NewO]) -> Pipe[I, NewO]:
        return Pipe(Composite(self.curr, next))

    def __call__(self, data: I) -> O:
        return self._execute(data)

    def _execute(self, __data: I) -> O:
        return self.curr(__data)
