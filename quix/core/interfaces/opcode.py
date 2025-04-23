from abc import abstractmethod
from collections.abc import Callable, Iterable
from typing import Any, ClassVar, Protocol, runtime_checkable

type OpcodeFactory[**P, O: Opcode] = Callable[P, O]


@runtime_checkable
class Opcode(Protocol):
    __slots__ = ()
    __id__: ClassVar[str]

    @abstractmethod
    def args(self) -> dict[str, Any]:
        raise NotImplementedError


@runtime_checkable
class Program[O: Opcode](Protocol, Iterable[O]): ...
