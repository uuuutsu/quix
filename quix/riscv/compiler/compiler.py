from inspect import signature
from typing import Any, Final, Self

from quix.bootstrap import ToConvert, convert
from quix.bootstrap.dtypes import Array, Unit, Wide
from quix.bootstrap.dtypes.const import UDynamic
from quix.bootstrap.macrocodes import switch_wide
from quix.bootstrap.program import SmartProgram
from quix.compiler.artifact.artifact import Artifact
from quix.compiler.compile import compile
from quix.core.opcodes import CoreOpcode, inject
from quix.core.opcodes.opcodes import add, end_loop, start_loop
from quix.exceptions.core.visitor import NoHandlerFoundException
from quix.riscv.compiler.instrs import get_instr
from quix.riscv.loader.opcodes import Imm, Register, RISCVOpcode
from quix.riscv.loader.state import State

_DEFAULT_SIZE: Final[int] = 84000

_DATA_SECTIONS: Final[tuple[str, ...]] = (
    ".rodata",
    ".sdata",
    ".data",
    ".sbss",
    ".bss",
    ".eh_frame",
    ".init_array",
    ".fini_array",
    ".symtab",
    ".strtab",
    ".shstrtab",
)


def _strip_data(data: bytes) -> tuple[bytes, int]:
    offset: int = 0
    while data and (data[0] == 0):
        offset += 1
        data = data[1:]
    return data or b"", offset


def _imm_to_const(imm: Imm) -> UDynamic:
    return UDynamic.from_int(imm, 4)


class Compiler:
    __slots__ = (
        "registers",
        "pc",
        "exit",
        "memory",
        "program",
    )

    def __init__(self) -> None:
        self.memory = Array("memory", length=_DEFAULT_SIZE)
        self.program = SmartProgram()
        self.registers = [Wide.from_length(f"x{idx}", 4) for idx in range(32)]
        self.pc = Wide.from_length("pc", 4)
        self.exit = Unit("exit")

    def run(self, state: State) -> Self:
        self._compile(state)
        return self

    def _compile(self, state: State) -> None:
        mapping: dict[UDynamic, CoreOpcode] = {}
        for _idx, (index, riscv_opcode) in enumerate(state.code.items()):
            mapping[UDynamic.from_int(index, 4)] = self._execute(riscv_opcode)
            print(f"Compiled: {riscv_opcode.__id__} ({_idx + 1}/{len(state.code)})")

        self.program |= self._compile_exec_loop(mapping)

    @convert
    def _compile_exec_loop(self, mapping: dict[UDynamic, CoreOpcode]) -> ToConvert:
        yield add(self.exit, 1)
        yield start_loop(self.exit)
        yield switch_wide(self.pc, mapping, else_=add(self.exit, -1))
        return end_loop()

    def _execute(self, opcode: RISCVOpcode) -> CoreOpcode:
        artifact = self._execute_opcode(opcode)
        return inject(None, artifact.code.code.getvalue(), None)

    def _execute_opcode(self, opcode: RISCVOpcode) -> Artifact:
        new_args = self._assemble_args(opcode)

        if custom_handler := get_instr(opcode.__id__):
            program = custom_handler(**new_args)
        else:
            raise NoHandlerFoundException(opcode, self)

        main_body = compile(program, gc=True, name=str(opcode))
        return main_body

    def _assemble_args(self, opcode: RISCVOpcode) -> dict[str, Any]:
        new_args: dict[str, Any] = {}

        for name, value in opcode.args().items():
            if isinstance(value, Imm):
                new_args[name] = _imm_to_const(value)
            elif isinstance(value, Register):
                new_args[name] = Wide.from_length(f"{name}_buff", 4)
            else:
                raise ValueError(f"Unknown argument type: {type(value)}")

        if custom_handler := get_instr(opcode.__id__):
            for name in signature(custom_handler).parameters:
                if name in ("memory", "pc", "exit"):
                    new_args[name] = getattr(self, name)
                if name.startswith("x"):
                    new_args[name] = self.registers[int(name[1:])]
        return new_args
