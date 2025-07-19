from __future__ import annotations

from collections.abc import Callable, Iterator
from logging import warning
from typing import ClassVar, Final, Self, get_args, overload

from quix.tools import FlyweightMeta

from .base import DType, dtype

CELL_SIZE: Final[int] = 8


@dtype
class Const[C](DType, metaclass=FlyweightMeta):
    value: C

    @classmethod
    def from_value(cls: type[Self], value: C) -> Self:
        return cls(cls.__name__, value=value)

    def __hash__(self) -> int:
        return hash(self.value)

    def __repr__(self) -> str:
        return str(self.value)

    def __str__(self) -> str:
        return f"{type(self).__name__}( {self.value} )"


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
        number >>= CELL_SIZE

    if not byte_list:
        return [0]

    return byte_list if little_endian else byte_list[::-1]


@dtype
class _Int(Const[int]):
    _MIN: ClassVar[int]
    _MAX: ClassVar[int]

    value: int

    def __post_init__(self) -> None:
        if not (self._MIN <= self.value <= self._MAX):
            new_value = _wrap(self.value, self._MIN, self._MAX)
            warning(
                f"{type(self).__name__}'s value must be in range [{self._MIN}, {self._MAX}]."
                f"\n\tPassed: {self.value}\n\tWrapped to: {new_value}"
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
class UCell(_Int):
    _MIN: ClassVar[int] = 0
    _MAX: ClassVar[int] = (1 << CELL_SIZE) - 1


@dtype
class Cell(_Int):
    _MIN: ClassVar[int] = -(1 << CELL_SIZE - 1)
    _MAX: ClassVar[int] = (1 << CELL_SIZE - 1) - 1


@dtype
class _DynamicInt[I: _Int](Const[tuple[I, ...]]):
    @property
    def size(self) -> int:
        return len(self.value)

    def __iter__(self) -> Iterator[I]:
        return self.value.__iter__()

    def __divmod__(self, other: _DynamicInt[I] | int) -> tuple[_DynamicInt[I], _DynamicInt[I]]:
        return self._op(other, lambda x, y: x // y), self._op(other, lambda x, y: x % y)

    def __sub__(self, other: _DynamicInt[I] | int) -> _DynamicInt[I]:
        return self._op(other, lambda x, y: x - y)

    def _op(self, other: _DynamicInt[I] | int, func: Callable[[int, int], int]) -> _DynamicInt[I]:
        if isinstance(other, int):
            new_value = func(int(self), other)
            return self.from_value(self.wrap(new_value))
        return self.from_int(func(int(self), int(other)), size=self.size)

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
        for int_ in self.value[::-1]:
            final_value <<= 8
            final_value += int(int_)
        return final_value

    @classmethod
    def from_int(cls, value: int, size: int | None = None) -> Self:
        ints_ = cls.wrap(value)
        if size is None:
            return cls.from_value(ints_)
        if len(ints_) == size:
            return cls.from_value(ints_[:size])
        elif len(ints_) > size:
            raise RuntimeError(f"Cannot store {value} in {size} cell(s).")

        int_cls: type[I] = get_args(cls.__orig_bases__[0])[0]  # type: ignore
        ints_ = ints_ + tuple(int_cls.from_value(0) for _ in range(size - len(ints_)))
        return cls.from_value(ints_)

    @classmethod
    def from_bytes(cls, value: bytes) -> Self:
        int_cls: type[I] = get_args(cls.__orig_bases__[0])[0]  # type: ignore
        ints_ = tuple(int_cls.from_value(val) for val in value)
        return cls.from_value(ints_)


@dtype
class UDynamic(_DynamicInt[UCell]): ...


@dtype
class Str(Const[str]):
    def __iter__(self) -> Iterator[str]:
        return self.value.__iter__()
