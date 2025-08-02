from dataclasses import asdict, dataclass
from typing import Any, Self, dataclass_transform

from quix.tools import statable


@dataclass_transform()
def dtype[C](cls: type[C]) -> type[C]:
    return dataclass(frozen=True)(cls)


@dtype
@statable
class DType:
    name: str

    def __repr__(self) -> str:
        return f"{type(self).__name__}( {self.name} )"

    def __hash__(self) -> int:
        raise NotImplementedError

    def __store__(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def __load__(cls, data: dict[str, Any]) -> Self:
        return cls(**data)
