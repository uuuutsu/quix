from io import StringIO

from quix.bootstrap.ast import reduce
from quix.bootstrap.ast.build import build_ast
from quix.bootstrap.program import ToConvert
from quix.cli.utils.error_handler import _error_exit
from quix.core.compiler.layout import BFMemoryLayout
from quix.core.compiler.pointer import BFPointer
from quix.core.compiler.visitor import BFVisitor
from quix.core.opcodes.dtypes import CoreProgram, Ref
from quix.memoptix import schedule


def _compile_to_bf(code: CoreProgram, mapping: dict[Ref, int]) -> str:
    buff = StringIO()
    memory_layout = BFMemoryLayout(mapping)
    pointer = BFPointer(memory_layout)
    BFVisitor(buff, pointer).visit(code)

    return buff.getvalue()


def _to_program(code: ToConvert) -> CoreProgram:
    return reduce(build_ast(code))


def compile(code: ToConvert, gc: bool = False) -> tuple[str, BFMemoryLayout]:
    core_program, mapping = schedule(_to_program(code), garbage_collector=gc)

    return _compile_to_bf(core_program, mapping), BFMemoryLayout(mapping)


def compile_seq(opcodes: ToConvert, gc: bool = False) -> tuple[str, BFMemoryLayout] | None:
    """
    Compiles sequence of opcodes to BrainFuck
    """
    try:
        return compile(opcodes, gc)

    except Exception as e:
        _error_exit(message="Unable to compile opcodes", exception=e)
        return None
