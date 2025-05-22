from abc import abstractmethod
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Statable(Protocol):
    __slots__ = ()

    @abstractmethod
    def __store__(self) -> dict[str, Any]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def __load__[C](cls: type[C], data: dict[str, Any]) -> C:
        raise NotImplementedError


def statable[C: Statable](cls: type[C]) -> type[C]:
    return cls
