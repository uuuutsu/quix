from __future__ import annotations

from collections.abc import Callable
from typing import Any

from multimethod import multidispatch, multimethod


class DynamicOverload[**P, R]:
    __slots__ = ("_dispatcher",)

    def __init__(
        self,
        func: Callable[P, R],
        *,
        dp: multimethod | None = None,
    ) -> None:
        self._dispatcher = dp or multidispatch(func)
        self._dispatcher.register(func)

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        return self._dispatcher(*args, **kwargs)  # type: ignore

    def __or__[**P_new, R_new](
        self,
        other: Callable[P_new, R_new] | DynamicOverload[P_new, R_new],
    ) -> DynamicOverload[P_new, R_new] | DynamicOverload[P, R]:
        return type(self)(other, dp=self._dispatcher)  # type: ignore


def dp_factory[**P, R](
    name: str,
    func: Callable[P, R],
    *,
    decs: list[Callable[[Callable[..., Any]], Callable[P, R]]] | None = None,
) -> DynamicOverload[P, R]:
    dp = multidispatch(func)

    dp.__name__ = name
    old_register = dp.register

    def _new_register(func: Callable[P, R]) -> Callable[P, R]:
        for dec in decs or []:
            func = dec(func)
        return old_register(func)

    dp.register = _new_register  # type: ignore
    return DynamicOverload(func, dp=dp)
