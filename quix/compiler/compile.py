from io import StringIO

from quix.bootstrap.reduce_program import reduce_program
from quix.core.compiler.layout import BFMemoryLayout
from quix.core.compiler.pointer import BFPointer
from quix.core.compiler.visitor import BFVisitor
from quix.core.opcodes.dtypes import CoreProgram, Ref
from quix.memoptix.schedule import schedule

from .artifact import Artifact, ArtifactCode, ArtifactHeader


def _schedule_program(program: CoreProgram, gc: bool) -> tuple[CoreProgram, dict[Ref, int]]:
    return schedule(reduce_program(program), garbage_collector=gc)


def _generate_bf_code(program: CoreProgram, mapping: dict[Ref, int]) -> StringIO:
    buffer = StringIO()
    layout = BFMemoryLayout(mapping)
    pointer = BFPointer(layout)
    BFVisitor(buffer, pointer).visit(program)
    return buffer


def _calculate_memory_stats(mapping: dict[Ref, int]) -> tuple[int, int]:
    if not mapping:
        return 0, 0
    memory_width = max(mapping.values()) + 1
    used_cells = len(set(mapping.values()))
    return memory_width, used_cells


def _determine_start_ptr(mapping: dict[Ref, int]) -> int:
    return min(mapping.values()) if mapping else 0


def _build_artifact(bf_code: StringIO, mapping: dict[Ref, int], name: str = "output") -> Artifact:
    memory_width, used_cells = _calculate_memory_stats(mapping)
    start_ptr = _determine_start_ptr(mapping)

    header = ArtifactHeader(start_ptr=start_ptr, memory_width=memory_width, used_cells=used_cells, memory=mapping)

    code = ArtifactCode(code=bf_code)
    return Artifact(header=header, code=code)


def compile(program: CoreProgram, gc: bool = True, name: str = "output") -> Artifact:
    scheduled_program, mapping = _schedule_program(program, gc)
    bf_code = _generate_bf_code(scheduled_program, mapping)
    return _build_artifact(bf_code, mapping, name)
