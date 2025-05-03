from typing import Final, override

import numpy as np

from quix.riscv.decompiler import State
from quix.riscv.executors.base import RISCVExecutor

from .memory import EmuMemory

_DATA_SECTIONS: Final[tuple[str, ...]] = (
    "rodata",
    "sdata",
    "data",
    "sbss",
    "bss",
    "eh_frame",
    "init_array",
    "fini_array",
    "symtab",
    "strtab",
    "shstrtab",
)


class Emulator(RISCVExecutor):
    __slots__ = (
        "memory",
        "registers",
        "pc",
        "csr",
    )

    def __init__(self) -> None:
        self.registers = np.array((32,), dtype=np.uint32)
        self.memory = EmuMemory()
        self.pc = 0
        self.csr: dict[int, int] = {}

    @override
    def run(self, state: State) -> None:
        self.pc = state.pc
        for name in _DATA_SECTIONS:
            if section := state.sections.get(name):
                self.memory[section.header["sh_addr"]] = section.data()  # type: ignore

        self.registers[1] = max(state.code) + 4
        self.registers[2] = 16000
        if sbss := state.sections.get(".sbss"):
            self.registers[3] = sbss.header["sh_addr"] + 2048
        self.registers[8] = 4048

        return super().run(state)

    @override
    def addi(self, imm: int, rs1: int, rd: int) -> None:
        self.registers[rd] = self.registers[rs1] + imm

    @override
    def sw(self, imm: int, rs1: int, rs2: int) -> None:
        self.memory[self.registers[rs1] + imm] = self.registers[rs2]

    @override
    def jal(self, imm: int, rd: int) -> None:
        self.registers[rd] = self.pc + 4
        self.pc += imm

    @override
    def lw(self, imm: int, rs1: int, rd: int) -> None:
        base_addr = self.registers[rs1] + imm
        self.registers[rd] = self.memory.get_word(base_addr)

    @override
    def andi(self, imm: int, rs1: int, rd: int) -> None:
        self.registers[rd] = self.registers[rs1] & imm

    @override
    def ori(self, imm: int, rs1: int, rd: int) -> None:
        self.registers[rd] = self.registers[rs1] | imm

    @override
    def xori(self, imm: int, rs1: int, rd: int) -> None:
        self.registers[rd] = self.registers[rs1] ^ imm

    @override
    def slli(self, imm: int, rs1: int, rd: int) -> None:
        self.registers[rd] = self.registers[rs1] << imm

    @override
    def srli(self, imm: int, rs1: int, rd: int) -> None:
        if (imm >> 6) > 0:
            value_to_shift = self.registers[rs1]

            if value_to_shift & 0x80000000:
                self.registers[rd] = (value_to_shift >> imm) | (0xFFFFFFFF << (32 - imm))

            self.registers[rd] = value_to_shift >> imm
            return

        self.registers[rd] = self.registers[rs1] >> imm

    @override
    def beq(self, imm: int, rs1: int, rs2: int) -> None:
        if self.registers[rs1] == self.registers[rs2]:
            self.pc += imm

    @override
    def bne(self, imm: int, rs1: int, rs2: int) -> None:
        if self.registers[rs1] != self.registers[rs2]:
            self.pc += imm

    @override
    def blt(self, imm: int, rs1: int, rs2: int) -> None:
        if self.registers[rs1] < self.registers[rs2]:
            self.pc += imm

    @override
    def bltu(self, imm: int, rs1: int, rs2: int) -> None:
        if self.registers[rs1] < self.registers[rs2]:
            self.pc += imm

    @override
    def bgeu(self, imm: int, rs1: int, rs2: int) -> None:
        if self.registers[rs1] >= self.registers[rs2]:
            self.pc += imm

    @override
    def lui(self, imm: int, rd: int) -> None:
        self.registers[rd] = imm

    @override
    def slti(self, imm: int, rs1: int, rd: int) -> None:
        self.registers[rd] = self.registers[rs1] < imm

    @override
    def sltiu(self, imm: int, rs1: int, rd: int) -> None:
        self.registers[rd] = (self.registers[rs1] & 0xFFFFFFFF) < (imm & 0xFFFFFFFF)

    @override
    def auipc(self, imm: int, rd: int) -> None:
        self.registers[rd] = self.pc + imm

    @override
    def bge(self, imm: int, rs1: int, rs2: int) -> None:
        if self.registers[rs1] >= self.registers[rs2]:
            self.pc += imm

    @override
    def jalr(self, imm: int, rs1: int, rd: int) -> None:
        temp = self.pc
        self.pc = (self.registers[rs1] + imm) & ~1
        self.registers[rd] = temp + 4

    @override
    def sb(self, imm: int, rs1: int, rs2: int) -> None:
        addr = self.registers[rs1] + imm
        self.memory[addr] = self.registers[rs2] & 0xFF

    @override
    def sh(self, imm: int, rs1: int, rs2: int) -> None:
        addr = self.registers[rs1] + imm
        self.memory[addr] = self.registers[rs2] & 0xFFFF

    @override
    def lb(self, imm: int, rs1: int, rd: int) -> None:
        addr = self.registers[rs1] + imm
        byte = self.memory[addr] & 0xFF

        if byte & 0x80:
            byte |= 0xFFFFFF00

        self.registers[rd] = byte

    @override
    def lbu(self, imm: int, rs1: int, rd: int) -> None:
        addr = self.registers[rs1] + imm
        self.registers[rd] = self.memory[addr] & 0xFF

    @override
    def lh(self, imm: int, rs1: int, rd: int) -> None:
        addr = self.registers[rs1] + imm
        hw = self.memory[addr] | (self.memory[addr + 1] << 8)
        hw |= 0xFFFF
        self.registers[rd] = hw

    @override
    def lhu(self, imm: int, rs1: int, rd: int) -> None:
        addr = self.registers[rs1] + imm
        value = self.memory[addr] | (self.memory[addr + 1] << 8)
        self.registers[rd] = value & 0xFFFF

    @override
    def add(self, rs1: int, rs2: int, rd: int) -> None:
        self.registers[rd] = self.registers[rs1] + self.registers[rs2]

    @override
    def sub(self, rs1: int, rs2: int, rd: int) -> None:
        self.registers[rd] = self.registers[rs1] - self.registers[rs2]

    @override
    def sll(self, rs1: int, rs2: int, rd: int) -> None:
        self.registers[rd] = self.registers[rs1] << (self.registers[rs2] & 0x1F)

    @override
    def slt(self, rs1: int, rs2: int, rd: int) -> None:
        self.registers[rd] = self.registers[rs1] < self.registers[rs2]

    @override
    def sltu(self, rs1: int, rs2: int, rd: int) -> None:
        self.registers[rd] = (self.registers[rs1] & 0xFFFFFFFF) < (self.registers[rs2] & 0xFFFFFFFF)

    @override
    def xor(self, rs1: int, rs2: int, rd: int) -> None:
        self.registers[rd] = self.registers[rs1] ^ self.registers[rs2]

    @override
    def srl(self, rs1: int, rs2: int, rd: int) -> None:
        self.registers[rd] = self.registers[rs1] >> (self.registers[rs2] & 0x1F)

    @override
    def sra(self, rs1: int, rs2: int, rd: int) -> None:
        value_to_shift = self.registers[rs1]
        shift_amount = self.registers[rs2] & 0x1F

        if value_to_shift & 0x80000000:
            self.registers[rd] = (value_to_shift >> shift_amount) | (0xFFFFFFFF << (32 - shift_amount))

        self.registers[rd] = value_to_shift >> shift_amount

    @override
    def or_(self, rs1: int, rs2: int, rd: int) -> None:
        self.registers[rd] = self.registers[rs1] | self.registers[rs2]

    @override
    def and_(self, rs1: int, rs2: int, rd: int) -> None:
        self.registers[rd] = self.registers[rs1] & self.registers[rs2]

    @override
    def fence(self, rs1: int, rs2: int, rd: int) -> None:
        pass  # Implement as needed

    @override
    def ecall(self, imm: int, rs1: int, rd: int) -> None:
        if imm > 0:
            exit()
        # Implement syscall handling

    @override
    def csrrw(self, imm: int, rs1: int, rd: int) -> None:
        old_value = self.csr.get(imm, 0)
        self.csr[imm] = self.registers[rs1]
        self.registers[rd] = old_value

    @override
    def csrrs(self, imm: int, rs1: int, rd: int) -> None:
        old_value = self.csr.get(imm, 0)
        self.csr[imm] = old_value | self.registers[rs1]
        self.registers[rd] = old_value

    @override
    def csrrwi(self, imm: int, rs1: int, rd: int) -> None:
        old_value = self.csr.get(imm, 0)
        self.csr[imm] = rs1
        self.registers[rd] = old_value

    @override
    def csrrsi(self, imm: int, rs1: int, rd: int) -> None:
        old_value = self.csr.get(imm, 0)
        self.csr[imm] = old_value | rs1
        self.registers[rd] = old_value

    @override
    def csrrci(self, imm: int, rs1: int, rd: int) -> None:
        old_value = self.csr.get(imm, 0)
        self.csr[imm] = old_value & ~rs1
        self.registers[rd] = old_value

    @override
    def mul(self, rs1: int, rs2: int, rd: int) -> None:
        self.registers[rd] = self.registers[rs1] * self.registers[rs2]

    @override
    def mulh(self, rs1: int, rs2: int, rd: int) -> None:
        result = (self.registers[rs1] * self.registers[rs2]) >> 32
        self.registers[rd] = result & 0xFFFFFFFF

    @override
    def mulhsu(self, rs1: int, rs2: int, rd: int) -> None:
        result = (self.registers[rs1] * self.registers[rs2]) >> 32
        self.registers[rd] = result & 0xFFFFFFFF

    @override
    def mulhu(self, rs1: int, rs2: int, rd: int) -> None:
        result = (self.registers[rs1] * self.registers[rs2]) >> 32
        self.registers[rd] = result & 0xFFFFFFFF

    @override
    def div(self, rs1: int, rs2: int, rd: int) -> None:
        self.registers[rd] = self.registers[rs1] // self.registers[rs2] if self.registers[rs2] != 0 else -1

    @override
    def divu(self, rs1: int, rs2: int, rd: int) -> None:
        self.registers[rd] = (
            (self.registers[rs1] & 0xFFFFFFFF) // (self.registers[rs2] & 0xFFFFFFFF)
            if self.registers[rs2] != 0
            else 0xFFFFFFFF
        )

    @override
    def rem(self, rs1: int, rs2: int, rd: int) -> None:
        self.registers[rd] = (
            self.registers[rs1] % self.registers[rs2] if self.registers[rs2] != 0 else self.registers[rs1]
        )

    @override
    def remu(self, rs1: int, rs2: int, rd: int) -> None:
        self.registers[rd] = (
            (self.registers[rs1] & 0xFFFFFFFF) % (self.registers[rs2] & 0xFFFFFFFF)
            if self.registers[rs2] != 0
            else self.registers[rs1] & 0xFFFFFFFF
        )
