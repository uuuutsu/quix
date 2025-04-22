from abc import abstractmethod
from collections.abc import Callable, Iterator
from typing import Any, ClassVar, Protocol

type OpcodeFactory[**P, O: Opcode] = Callable[P, O]


class Opcode(Protocol):
    __slots__ = ()
    __id__: ClassVar[str]

    @abstractmethod
    def args(self) -> dict[str, Any]:
        raise NotImplementedError


class Program[O: Opcode](Protocol, Iterator[O]): ...
