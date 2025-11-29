from typing import Any, Final, Self

from quix.bootstrap.dtypes import Array, Unit, Wide
from quix.bootstrap.dtypes.const import UDynamic
from quix.bootstrap.program import SmartProgram
from quix.compiler.artifact.artifact import Artifact
from quix.compiler.compile import compile
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
        self.registers = [Wide.from_length(f"reg_{idx}", 4) for idx in range(32)]
        self.pc = Wide.from_length("pc", 4)
        self.exit = Unit("exit")

    def run(self, state: State) -> Self:
        self._compile_exec_loop(state)
        return self

    def _compile_exec_loop(self, state: State) -> None:
        mapping: dict[UDynamic, Artifact] = {}
        print(f"Found: {len(state.code)} instructions")
        for _idx, (index, riscv_opcode) in enumerate(state.code.items()):
            mapping[UDynamic.from_int(index, 4)] = artifact = self._execute(riscv_opcode)
            print(artifact)
            return
            print(f"Compiled: {riscv_opcode.__id__} ({_idx + 1}/{len(state.code)})")

        # self.program |= self.cpu.run(mapping)

    def _execute(self, opcode: RISCVOpcode) -> Artifact:
        new_args: dict[str, Any] = {}

        for name, value in opcode.args().items():
            if isinstance(value, Imm):
                new_args[name] = _imm_to_const(value)
            elif isinstance(value, Register):
                new_args[name] = Wide.from_length(f"{name}_buff", 4)
            else:
                raise ValueError(f"Unknown argument type: {type(value)}")

        if custom_handler := get_instr(opcode.__id__):
            program = custom_handler(**new_args)
        else:
            raise NoHandlerFoundException(opcode, self)

        artifact = compile(program, gc=True, name=str(opcode))
        return artifact
