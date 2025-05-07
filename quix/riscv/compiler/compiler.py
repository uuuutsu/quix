from typing import Final

from quix.bootstrap.dtypes.const import DynamicUInt
from quix.bootstrap.program import SmartProgram
from quix.riscv.loader.state import State
from quix.riscv.opcodes.executor import RISCVExecutor

from .runtime import CPU, Memory

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


class Compiler(RISCVExecutor):
    __slots__ = (
        "cpu",
        "memory",
        "program",
    )

    def __init__(self) -> None:
        self.cpu = CPU()
        self.memory = Memory()
        self.program = SmartProgram()

    def run(self, state: State) -> None:
        self._init_cpu(state)
        self._init_memory(state)
        self._init_memory(state)

    def _init_cpu(self, state: State) -> None:
        self.program |= self.cpu.set_pc(DynamicUInt.from_int(state.entry, size=4))

    def _init_memory(self, state: State) -> None:
        for name in _DATA_SECTIONS:
            if section := state.sections.get(name):
                self.program |= self.memory.store(
                    DynamicUInt.from_int(section.header["sh_addr"]),
                    section.data(),  # type: ignore
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
