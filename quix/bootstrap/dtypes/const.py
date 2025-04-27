from quix.tools import FlyweightMeta

from .base import DType, dtype


@dtype
class Const[C](DType, metaclass=FlyweightMeta):
    value: C


@dtype
class Int8(Const[int]):
    value: int

    def __post_init__(self) -> None:
        if self.value not in range(0, 256):
            raise ValueError(f"Int8 can only be in range [0, 255]. Got: {self.value}")
