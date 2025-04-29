from collections.abc import Callable
from functools import wraps
from inspect import signature
from typing import Any


class Arg:
    __slots__ = ("name", "_callbacks")

    def __init__(self, name: str) -> None:
        self.name = name
        self._callbacks: list[Callable[[Any], None]] = []

    def __call__(self, data: dict[str, Any]) -> None:
        if (value := data.get(self.name)) is None:
            raise ValueError(f"Argument {self.name!r} not found in {data}")
        for callback in self._callbacks:
            callback(value)


def check[**P, R](*checks_: Callable[[dict[str, Any]], None]) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def _wrapper(func: Callable[P, R]) -> Callable[P, R]:
        sign = signature(func)

        @wraps(func)
        def _inner(*args: P.args, **kwargs: P.kwargs) -> R:
            binded = sign.bind(*args, **kwargs)
            binded.apply_defaults()
            for check_ in checks_:
                check_(binded.arguments)
            return func(*args, **kwargs)

        return _inner

    return _wrapper
