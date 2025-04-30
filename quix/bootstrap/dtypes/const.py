from __future__ import annotations

from collections.abc import Callable, Iterator
from logging import warning
from typing import ClassVar, Self, get_args, overload

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


def _int_to_cell_size(number: int, *, little_endian: bool = False) -> list[int]:
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

    def __int__(self) -> int:
        return self.value + self._MIN

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
class _DynamicInt[I: _Int](Const[tuple[I, ...]]):
    @property
    def size(self) -> int:
        return len(self.value)

    def __iter__(self) -> Iterator[I]:
        return self.value.__iter__()

    def __divmod__[C: _DynamicInt[I]](self: C, other: C | int) -> tuple[C, C]:
        return self._op(other, lambda x, y: x // y), self._op(other, lambda x, y: x % y)

    def _op[C: _DynamicInt[I]](self: C, other: C | int, func: Callable[[int, int], int]) -> C:
        if isinstance(other, int):
            new_value = func(int(self), other)
            return self.from_value(self.wrap(new_value))
        return self.from_value(self.wrap(func(int(self), int(other))))

    @overload
    def __getitem__(self, item: int) -> I: ...
    @overload
    def __getitem__(self, item: slice) -> tuple[I, ...]: ...
    def __getitem__(self, item: int | slice) -> I | tuple[I, ...]:
        return self.value[item]

    @classmethod
    def wrap(cls, value: int) -> tuple[I, ...]:
        int_cls: type[I] = get_args(cls.__orig_bases__[0])[0]  # type: ignore
        return tuple(int_cls.from_value(int_) for int_ in _int_to_cell_size(value))

    def __int__(self) -> int:
        final_value: int = 0
        for int_ in self.value:
            final_value <<= 8
            final_value += int(int_)
        return final_value

    @classmethod
    def from_int(cls, value: int, size: int | None = None) -> Self:
        ints_ = cls.wrap(value)
        if size is None:
            return cls.from_value(ints_)
        if len(ints_) > size:
            return cls.from_value(ints_[:size])

        int_cls: type[I] = get_args(cls.__orig_bases__[0])[0]  # type: ignore
        ints_ = tuple(int_cls.from_value(0) for _ in range(size - len(ints_))) + ints_
        return cls.from_value(ints_)


@dtype
class DynamicUInt(_DynamicInt[UInt8]): ...


@dtype
class DynamicInt(_DynamicInt[Int8]): ...
