from typing import Self

from quix.tools import FlyweightMeta

from .base import DType, dtype


@dtype
class Const[C](DType, metaclass=FlyweightMeta):
    value: C

    @classmethod
    def from_value(cls: type[Self], value: C) -> Self:
        return cls("const", value=value)


@dtype
class UInt8(Const[int]):
    value: int

    def __post_init__(self) -> None:
        if self.value not in range(0, 256):
            raise ValueError(f"UInt8 can only be in range [0, 255]. Got: {self.value}")


@dtype
class Int8(Const[int]):
    value: int

    def __post_init__(self) -> None:
        if self.value not in range(-128, 128):
            raise ValueError(f"Int8 can only be in range [-128, 128]. Got: {self.value}")
