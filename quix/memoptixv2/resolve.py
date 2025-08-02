from quix.core.opcodes.dtypes import CoreProgram, Ref

from .compile import program_to_trees
from .scheduler import Scheduler
from .scheduler.resolvers import create_resolver_registry
from .scheduler.sliders import create_slider_registry


def resolve(program: CoreProgram) -> tuple[CoreProgram, dict[Ref, int]]:
    trees = program_to_trees(program)
    layout = Scheduler(create_resolver_registry(), create_slider_registry()).schedule(*trees)

    memory = {node.ref: index for node, index in layout.mapping().items()}
    return program, memory
