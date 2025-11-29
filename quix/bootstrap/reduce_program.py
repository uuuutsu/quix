from quix.bootstrap.macrocode import MacroCode
from quix.bootstrap.program import SmartProgram, ToConvert, to_program


def reduce_program(program: ToConvert) -> SmartProgram:
    result = SmartProgram()
    for opcode in to_program(program):
        if isinstance(opcode, MacroCode):
            result |= reduce_program(to_program(opcode()).build())
        else:
            result |= opcode
    return result
