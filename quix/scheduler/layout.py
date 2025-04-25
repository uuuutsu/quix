from rich.pretty import pretty_repr

from .owner import Owner


class Layout:
    __slots__ = (
        "_mapping",
        "absolute",
    )

    def __init__(self, absolute: bool = False) -> None:
        self._mapping: dict[Owner, int] = {}
        self.absolute = absolute

    def set(self, key: Owner, value: int) -> None:
        self._mapping[key] = value

    def mapping(self) -> dict[Owner, int]:
        return self._mapping

    def __repr__(self) -> str:
        return pretty_repr(self._mapping)
