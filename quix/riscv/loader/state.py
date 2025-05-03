from dataclasses import dataclass

from elftools.elf.sections import Section

from quix.riscv.opcodes.base import RISCVOpcode


@dataclass
class State:
    code: dict[int, RISCVOpcode]
    entry: int
    sections: dict[str, Section]
