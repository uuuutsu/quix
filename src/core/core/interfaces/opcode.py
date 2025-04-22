from abc import abstractmethod
from typing import Any, Protocol


class Opcode(Protocol):
    @abstractmethod
    def attrs(self) -> dict[str, Any]:
        raise NotImplementedError


