from dataclasses import dataclass
from enum import IntEnum, StrEnum

from quix.core.opcodes.dtypes import Ref


class CellSize(IntEnum):
    BYTE = 8


class BFVariant(StrEnum):
    VANILLA = "vanilla"


@dataclass
class DataCell:
    name: str
    idx: int
    description: str | None = None


@dataclass
class ArtifactHeader:
    start_ptr: int
    memory_width: int
    used_cells: int
    inputs: list[DataCell] | None = None
    outputs: list[DataCell] | None = None
    description: str | None = None
    cell_size: CellSize = CellSize.BYTE
    bf_variant: BFVariant = BFVariant.VANILLA
    memory: dict[Ref, int] | None = None
