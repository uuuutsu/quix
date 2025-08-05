from quix.core.opcodes.dtypes import CoreProgram, Ref

from .compile import program_to_trees
from .opcodes import MemoptixOpcodes
from .scheduler import Scheduler
from .scheduler.resolvers import create_resolver_registry
from .scheduler.sliders import create_slider_registry


def schedule(program: CoreProgram, garbage_collector: bool = True) -> tuple[CoreProgram, dict[Ref, int]]:
    trees = program_to_trees(program, garbage_collector)
    layout = Scheduler(create_resolver_registry(), create_slider_registry()).schedule(*trees)

    memory = {node.ref: index for node, index in layout.mapping().items()}
    return strip_memoptix_opcodes(program), memory


def strip_memoptix_opcodes(program: CoreProgram) -> CoreProgram:
    return [opcode for opcode in program if opcode.__id__ not in MemoptixOpcodes]
