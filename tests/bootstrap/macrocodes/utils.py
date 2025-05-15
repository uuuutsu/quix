from io import StringIO

from quix.bootstrap.program import ToConvert
from quix.bootstrap.reducer import reduce
from quix.core.compiler.layout import BFMemoryLayout
from quix.core.compiler.pointer import BFPointer
from quix.core.compiler.visitor import BFVisitor
from quix.core.opcodes.dtypes import CoreProgram, Ref
from quix.exec.simple import Executor
from quix.memoptix import mem_compile


def run_with_output(code: ToConvert) -> str:
    core_program, mapping = mem_compile(reduce(code), garbage_collector=False)
    code = _compile_to_bf(core_program, mapping)
    output = StringIO()
    Executor(code, output=output).run()
    return output.getvalue()


def run_with_tape(code: ToConvert) -> tuple[dict[Ref, int], list[int]]:
    core_program, mapping = mem_compile(reduce(code), garbage_collector=False)
    code = _compile_to_bf(core_program, mapping)

    executor = Executor(code).run()
    memory = executor.memory.cells

    return mapping, memory


def run(code: ToConvert) -> dict[Ref, int]:
    core_program, mapping = mem_compile(reduce(code), garbage_collector=False)
    code = _compile_to_bf(core_program, mapping)
    # print(code, len(code))
    executor = Executor(code).run()
    memory = executor.memory.cells
    values = {ref: memory[idx] for ref, idx in mapping.items()}

    return values


def _compile_to_bf(code: CoreProgram, mapping: dict[Ref, int]) -> str:
    buff = StringIO()
    pointer = BFPointer(BFMemoryLayout(mapping))
    BFVisitor(buff, pointer).visit(code)

    return buff.getvalue()
