from typing import Final, Self

from quix.bootstrap.dtypes.const import DynamicUInt
from quix.bootstrap.program import SmartProgram, ToConvert, to_program
from quix.core.opcodes.dtypes import CoreProgram
from quix.exceptions.core.visitor import NoHandlerFoundException
from quix.riscv.loader.state import State
from quix.riscv.opcodes.base import RISCVOpcode
from quix.riscv.opcodes.executor import RISCVExecutor

from .runtime import CPU, Layout, Memory

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


class Compiler(RISCVExecutor[ToConvert]):
    __slots__ = (
        "cpu",
        "memory",
        "program",
    )

    def __init__(self) -> None:
        self.cpu = CPU()
        self.memory = Memory()
        self.program = SmartProgram()
        self._init_runtime()

    def run(self, state: State) -> Self:
        self._init_cpu(state)
        self._init_registers(state)
        self._init_memory(state)
        self._compile_exec_loop(state)
        return self

    def _init_runtime(self) -> None:
        self.program |= Layout().add_component(self.cpu, 0).add_component(self.memory, 0).create(50)

    def _init_cpu(self, state: State) -> None:
        self.program |= self.cpu.set_pc(DynamicUInt.from_int(state.entry, size=4))

    def _init_memory(self, state: State) -> None:
        for name in _DATA_SECTIONS:
            if section := state.sections.get(name):
                data, offset = _strip_data(section.data())  # type: ignore
                if not data:
                    continue
                self.program |= self.memory.store(
                    DynamicUInt.from_int(section.header["sh_addr"] + offset),
                    DynamicUInt.from_bytes(data),
                )

    def _init_registers(self, state: State) -> None:
        self.program |= self.cpu.store_register(
            DynamicUInt.from_int(1),
            DynamicUInt.from_int(max(state.code) + 4),
        )
        self.program |= self.cpu.store_register(
            DynamicUInt.from_int(2),
            DynamicUInt.from_int(16000),
        )
        if sbss := state.sections.get(".sbss"):
            self.program |= self.cpu.store_register(
                DynamicUInt.from_int(3),
                DynamicUInt.from_int(sbss.header["sh_addr"] + 2048),
            )
        self.program |= self.cpu.store_register(
            DynamicUInt.from_int(8),
            DynamicUInt.from_int(4048),
        )

    def _compile_exec_loop(self, state: State) -> None:
        mapping: dict[DynamicUInt, CoreProgram] = {}
        for index, riscv_opcode in state.code.items():
            mapping[DynamicUInt.from_int(index, 4)] = self._execute(riscv_opcode)

        self.program |= self.cpu.run(mapping)

    def _execute(self, opcode: RISCVOpcode) -> CoreProgram:
        if (method := getattr(self, opcode.__id__, None)) is None:
            raise NoHandlerFoundException(opcode, self)

        return to_program(method(**opcode.args()))
