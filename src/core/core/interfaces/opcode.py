from abc import abstractmethod
from typing import Any, Callable, ClassVar, Iterator, Protocol

type OpcodeFactory[**P, O: Opcode] = Callable[P, O]


class Opcode(Protocol):
    __id__: ClassVar[str]

    @abstractmethod
    def args(self) -> dict[str, Any]:
        raise NotImplementedError


class Program[O: Opcode](Protocol, Iterator[O]): ...
