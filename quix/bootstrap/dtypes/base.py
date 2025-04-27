from dataclasses import dataclass

dtype = dataclass(slots=True, frozen=True)


@dtype
class DType:
    name: str

    def __repr__(self) -> str:
        return f"{type(self).__name__}( {self.name} )"
