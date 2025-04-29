from __future__ import annotations

from collections.abc import Callable, Iterator
from logging import warning
from typing import ClassVar, Self

from quix.tools import FlyweightMeta

from .base import DType, dtype


@dtype
class Const[C](DType, metaclass=FlyweightMeta):
    value: C

    @classmethod
    def from_value(cls: type[Self], value: C) -> Self:
        return cls(f"Const( {value} )", value=value)


def _wrap(value: int, min: int, max: int) -> int:
    range = max - min + 1
    value -= min
    value %= range
    value += min
    return value


def _int_to_cell_size(number: int, *, little_endian: bool = True) -> list[int]:
    byte_list = []
    while number > 0:
        byte_list.append(number & 0xFF)
        number >>= 8

    if not byte_list:
        return [0]

    return byte_list[::-1] if little_endian else byte_list


@dtype
class _Int(Const[int]):
    _MIN: ClassVar[int]
    _MAX: ClassVar[int]

    value: int

    def __post_init__(self) -> None:
        if not (self._MIN <= self.value <= self._MAX):
            new_value = _wrap(self.value, self._MIN, self._MAX)
            warning(
                f"{type(self).__name__}'s value must be in range [{self._MIN}, {self._MIN}]."
                "\n\tPassed: {self.value}\n\tWrapped to: {new_value}"
            )
            object.__setattr__(self, "value", new_value)

    def __mul__[C: _Int](self: C, other: C | int) -> C:
        return self._op(other, lambda x, y: x * y)

    def __add__[C: _Int](self: C, other: C | int) -> C:
        return self._op(other, lambda x, y: x + y)

    def __sub__[C: _Int](self: C, other: C | int) -> C:
        return self._op(other, lambda x, y: x - y)

    def __divmod__[C: _Int](self: C, other: C | int) -> tuple[C, C]:
        return self._op(other, lambda x, y: x // y), self._op(other, lambda x, y: x % y)

    def __invert__[C: _Int](self: C) -> C:
        return self.from_value(self.wrap(~self.value))

    def _op[C: _Int](self: C, other: C | int, func: Callable[[int, int], int]) -> C:
        if isinstance(other, int):
            return self.from_value(self.wrap(func(self.value, other)))
        return self.from_value(self.wrap(func(self.value, other.value)))

    def to[C: _Int](self, other: type[C]) -> C:
        return other.from_value(other.wrap(self.value))

    @classmethod
    def wrap(cls, value: int) -> int:
        return _wrap(value, cls._MIN, cls._MAX)


@dtype
class UInt8(_Int):
    _MIN: ClassVar[int] = 0
    _MAX: ClassVar[int] = 255


@dtype
class Int8(_Int):
    _MIN: ClassVar[int] = -128
    _MAX: ClassVar[int] = 127


@dtype
class DynamicUInt(Const[int]):
    @property
    def size(self) -> int:
        return len(_int_to_cell_size(self.value))

    def __iter__(self) -> Iterator[UInt8]:
        for int_ in _int_to_cell_size(self.value):
            yield UInt8.from_value(int_)
