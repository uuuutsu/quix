from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from inspect import signature
from typing import Any

type Callback = Callable[[Context], Context]


@dataclass
class Context:
    curr_value: Any
    data: dict[str, Any]


def _get_private_name_prefix(obj: object) -> str:
    return f"_{type(obj).__name__}__"


def _extract_me(name: str) -> Callback:
    def _inner(context: Context) -> Context:
        if name not in context.curr_value:
            raise ValueError(f"{name!r} not found in arguments {context.curr_value}.")
        return Context(context.curr_value[name], context.data)

    return _inner


def _func_passthrough[**P, R_left, R_right](
    left: Callable[P, R_left], right: Callable[[R_left], R_right]
) -> Callable[P, R_right]:
    def _inner(*args: P.args, **kwargs: P.kwargs) -> R_right:
        return right(left(*args, **kwargs))

    return _inner


class Arg:
    __slots__ = (
        "__name",
        "__callback",
    )
    __callback: Callback

    def __init__(self, name: str, *, callback: Callback | None = None) -> None:
        self.__name = name
        self.__callback = callback or _extract_me(name)

    def __call__(self, data: dict[str, Any]) -> Context:
        return self.__callback(Context(data, data))

    def __getattribute__(self, name: str) -> Arg:
        if name.startswith(_get_private_name_prefix(self)):
            return super().__getattribute__(name)  # type: ignore

        def _get_attr(self_value: Context) -> Context:
            return Context(getattr(self_value.curr_value, name), self_value.data)

        return Arg(name, callback=_func_passthrough(self.__callback, _get_attr))

    def __eq__(self, other: object) -> Arg:  # type: ignore
        def _eq(context: Context) -> Context:
            other_value = other(context.data).curr_value if isinstance(other, Arg) else other
            if other_value != context.curr_value:
                raise ValueError(f"{self} validation error: {other_value} != {context.curr_value}")
            return Context(context.curr_value, context.data)

        return Arg(self.__name, callback=_func_passthrough(self.__callback, _eq))

    def __repr__(self) -> str:
        return f"{type(self).__name__}( {self.__name!r} )"


def check[**P, R](*checks_: Callable[[dict[str, Any]], Any]) -> Callable[[Callable[P, R]], Callable[P, R]]:
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
