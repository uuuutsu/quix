from __future__ import annotations

from collections.abc import Callable
from typing import Any, NoReturn

from multimethod import multidispatch, multimethod


def _dummy() -> NoReturn:
    raise NotImplementedError("https://media.tenor.com/GNAQm8mZEPgAAAAM/oppenheimer-cillian-murphy.gif")


class DynamicOverload[**P, R]:
    __slots__ = ("_dispatcher",)

    def __init__(
        self,
        func: Callable[P, R] | None = None,
        *,
        dp: multimethod | None = None,
    ) -> None:
        if dp is None:
            self._dispatcher = multidispatch(func or _dummy)
            return

        self._dispatcher = dp
        dp.register(func or _dummy)

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        return self._dispatcher(*args, **kwargs)

    def __or__[**P_new, R_new](
        self,
        other: Callable[P_new, R_new] | DynamicOverload[P_new, R_new],
    ) -> DynamicOverload[P, R] | DynamicOverload[P_new, R_new]:
        return type(self)(other, dp=self._dispatcher)  # type: ignore


def dp_factory[**P, R](
    name: str,
    *,
    decs: list[Callable[[Callable[..., Any]], Callable[P, R]]] | None = None,
) -> DynamicOverload[[], NoReturn]:
    dp = multidispatch(_dummy)

    dp.__name__ = name
    old_register = dp.register

    def _new_register(func: Callable[P, R]) -> Callable[P, R]:
        for dec in decs or []:
            func = dec(func)
        return old_register(func)

    dp.register = _new_register  # type: ignore
    return DynamicOverload(_dummy, dp=dp)
