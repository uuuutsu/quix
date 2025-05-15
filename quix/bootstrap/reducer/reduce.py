from quix.bootstrap.macrocode import MacroCode
from quix.bootstrap.program import SmartProgram, ToConvert, to_program
from quix.core.opcodes.dtypes import CoreProgram


def reduce(code: ToConvert) -> CoreProgram:
    return _iterative_compiler(code)


def _iterative_compiler(code: ToConvert) -> CoreProgram:
    program: SmartProgram = SmartProgram()
    reduce: bool = False
    for opcode in to_program(code):
        if isinstance(opcode, MacroCode):
            program |= opcode()
            reduce = True
        else:
            program |= opcode

    program = _optimize_iteration(program)
    if reduce:
        return _iterative_compiler(program)

    return program


def _optimize_iteration[P: CoreProgram](program: P) -> P:
    return program
