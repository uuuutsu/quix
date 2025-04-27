from dataclasses import dataclass
from typing import dataclass_transform


@dataclass_transform()
def dtype[C](cls: type[C]) -> type[C]:
    return dataclass(slots=True, frozen=True)(cls)


@dtype
class DType:
    name: str

    def __repr__(self) -> str:
        return f"{type(self).__name__}( {self.name} )"
