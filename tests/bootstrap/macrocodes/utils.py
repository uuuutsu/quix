from io import StringIO

from quix.bootstrap.ast import reduce
from quix.bootstrap.ast.build import build_ast
from quix.bootstrap.program import ToConvert
from quix.core.compiler.layout import BFMemoryLayout
from quix.core.compiler.pointer import BFPointer
from quix.core.compiler.visitor import BFVisitor
from quix.core.opcodes.dtypes import CoreProgram, Ref
from quix.exec.simple import Executor
from quix.memoptix.schedule import schedule


def run_with_output(code: ToConvert) -> str:
    core_program, mapping = schedule(_to_program(code), garbage_collector=False)
    code_str = _compile_to_bf(core_program, mapping)
    output = StringIO()
    Executor(code_str, output=output).run()
    return output.getvalue()


def run_with_tape(code: ToConvert) -> tuple[dict[Ref, int], list[int]]:
    core_program, mapping = schedule(_to_program(code), garbage_collector=False)
    code_str = _compile_to_bf(core_program, mapping)

    executor = Executor(code_str).run()
    memory = executor.memory.cells

    return mapping, memory


def run(code: ToConvert) -> dict[Ref, int]:
    core_program, mapping = schedule(_to_program(code), garbage_collector=False)
    code_str = _compile_to_bf(core_program, mapping)

    executor = Executor(code_str).run()
    memory = executor.memory.cells
    values = {ref: memory[idx] for ref, idx in mapping.items()}

    return values


def _compile_to_bf(code: CoreProgram, mapping: dict[Ref, int]) -> str:
    buff = StringIO()
    pointer = BFPointer(BFMemoryLayout(mapping))
    BFVisitor(buff, pointer).visit(code)

    return buff.getvalue()


def _to_program(code: ToConvert) -> CoreProgram:
    return reduce(build_ast(code))
