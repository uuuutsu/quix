__all__ = (
    "BaseSection",
    "Section",
    "Immediate",
    #
    "I_Imm",
    "S_Imm",
    "B_Imm",
    "U_Imm",
    "J_Imm",
)

from abc import ABC, abstractmethod
from dataclasses import dataclass

from .utils import get_bit_section


class BaseSection(ABC):
    __slots__ = ()

    @abstractmethod
    def decode(self, instruction: int) -> int:
        raise NotImplementedError


@dataclass(slots=True)
class Section(BaseSection):
    start: int
    end: int

    def decode(self, instr: int) -> int:
        return get_bit_section(instr, self.start, self.end)


@dataclass(slots=True)
class Immediate(BaseSection):
    sec2offset: dict[tuple[int, int], int]
    n_bits: int

    # The index of sign bit in the instruction. As RISC-V ISA specifies it's always the 31st
    sign_bit: int = 31

    def decode(self, instruction: int) -> int:
        immediate = 0

        for instr_itv, int_offset in self.sec2offset.items():
            instr_val = get_bit_section(instruction, *instr_itv)
            immediate += instr_val << int_offset

        if get_bit_section(instruction, self.sign_bit, self.sign_bit):
            return immediate | (-1 << self.n_bits - 1)

        return immediate


I_Imm = Immediate(
    sec2offset={
        (30, 20): 0,
    },
    n_bits=12,
)
S_Imm = Immediate(
    sec2offset={
        (30, 25): 5,
        (11, 8): 1,
        (7, 7): 0,
    },
    n_bits=12,
)
B_Imm = Immediate(
    sec2offset={
        (7, 7): 11,
        (30, 25): 5,
        (11, 8): 1,
    },
    n_bits=12,
)
U_Imm = Immediate(
    sec2offset={
        (30, 12): 12,
    },
    n_bits=20,
)
J_Imm = Immediate(
    sec2offset={
        (19, 12): 12,
        (20, 20): 11,
        (30, 25): 5,
        (24, 21): 1,
    },
    n_bits=20,
)
