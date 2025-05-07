from typing import Final, Self, override

import numpy as np

from quix.riscv.loader import State
from quix.riscv.loader.decoder.utils import get_bit_section
from quix.riscv.opcodes import Imm, Register, RISCVExecutor

from .memory import Memory

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


class Emulator(RISCVExecutor):
    __slots__ = ("memory", "registers", "pc", "csr", "brk")

    def __init__(self) -> None:
        self.registers = np.zeros((32,), dtype=np.int32)
        self.memory = Memory()
        self.pc = 0
        self.csr: dict[int, int] = {}
        self.brk: int = 0

    def run(self, state: State) -> Self:
        self.pc = state.entry
        for name in _DATA_SECTIONS:
            if section := state.sections.get(name):
                self.memory[section.header["sh_addr"]] = section.data()  # type: ignore

        self.registers[1] = max(state.code) + 4
        self.registers[2] = 16000
        if sbss := state.sections.get(".sbss"):
            self.registers[3] = sbss.header["sh_addr"] + 2048
        self.registers[8] = 4048

        while True:
            prev_pc = self.pc

            try:
                code = state.code[self.pc]
                getattr(self, code.__id__)(**code.args())
            except KeyError:
                print(self.pc, self.pc + 4)
                print(self.registers)
                break

            if prev_pc == self.pc:
                self.pc += 4
            self.registers[0] = 0
        return self

    @override
    def addi(self, imm: Imm, rs1: Register, rd: Register) -> None:
        self.registers[rd] = self.registers[rs1] + imm

    @override
    def sw(self, imm: Imm, rs1: Register, rs2: Register) -> None:
        self.memory[self.registers[rs1] + imm] = [
            self.registers[rs2] & 0xFF,
            (self.registers[rs2] >> 8) & 0xFF,
            (self.registers[rs2] >> 16) & 0xFF,
            (self.registers[rs2] >> 24) & 0xFF,
        ]

    @override
    def jal(self, imm: Imm, rd: Register) -> None:
        self.registers[rd] = self.pc + 4
        self.pc += imm

    @override
    def lw(self, imm: Imm, rs1: Register, rd: Register) -> None:
        number = self.memory[self.registers[rs1] + imm]
        number |= self.memory[self.registers[rs1] + imm + 1] << 8
        number |= self.memory[self.registers[rs1] + imm + 2] << 16
        number |= self.memory[self.registers[rs1] + imm + 3] << 24
        self.registers[rd] = np.int32(number)

    @override
    def andi(self, imm: Imm, rs1: Register, rd: Register) -> None:
        self.registers[rd] = self.registers[rs1] & imm

    @override
    def ori(self, imm: Imm, rs1: Register, rd: Register) -> None:
        self.registers[rd] = self.registers[rs1] | imm

    @override
    def xori(self, imm: Imm, rs1: Register, rd: Register) -> None:
        self.registers[rd] = self.registers[rs1] ^ imm

    @override
    def slli(self, imm: Imm, rs1: Register, rd: Register) -> None:
        self.registers[rd] = self.registers[rs1] << (imm & 0x1F)

    @override
    def srli(self, imm: Imm, rs1: Register, rd: Register) -> None:
        if get_bit_section(imm, 10, 10):
            self.registers[rd] = self.registers[rs1] >> (imm & 0x1F)
            return

        self.registers[rd] = np.uint32(self.registers[rs1]) >> (imm & 0x1F)

    @override
    def beq(self, imm: Imm, rs1: Register, rs2: Register) -> None:
        if self.registers[rs1] == self.registers[rs2]:
            self.pc += imm

    @override
    def bne(self, imm: Imm, rs1: Register, rs2: Register) -> None:
        if self.registers[rs1] != self.registers[rs2]:
            self.pc += imm

    @override
    def blt(self, imm: Imm, rs1: Register, rs2: Register) -> None:
        if self.registers[rs1] < self.registers[rs2]:
            self.pc += imm

    @override
    def bltu(self, imm: Imm, rs1: Register, rs2: Register) -> None:
        if np.uint32(self.registers[rs1]) < np.uint32(self.registers[rs2]):
            self.pc += imm

    @override
    def bgeu(self, imm: Imm, rs1: Register, rs2: Register) -> None:
        if np.uint32(self.registers[rs1]) >= np.uint32(self.registers[rs2]):
            self.pc += imm

    @override
    def lui(self, imm: Imm, rd: Register) -> None:
        self.registers[rd] = imm

    @override
    def slti(self, imm: Imm, rs1: Register, rd: Register) -> None:
        self.registers[rd] = self.registers[rs1] < imm

    @override
    def sltiu(self, imm: Imm, rs1: Register, rd: Register) -> None:
        self.registers[rd] = np.uint32(self.registers[rs1]) < np.uint32(imm)

    @override
    def auipc(self, imm: Imm, rd: Register) -> None:
        self.registers[rd] = self.pc + imm

    @override
    def bge(self, imm: Imm, rs1: Register, rs2: Register) -> None:
        if self.registers[rs1] >= self.registers[rs2]:
            self.pc += imm

    @override
    def jalr(self, imm: Imm, rs1: Register, rd: Register) -> None:
        temp = self.pc
        self.pc = int(np.uint32(self.registers[rs1] + imm) & ~np.uint32(1))
        self.registers[rd] = temp + 4

    @override
    def sb(self, imm: Imm, rs1: Register, rs2: Register) -> None:
        self.memory[self.registers[rs1] + imm] = [
            self.registers[rs2] & 0xFF,
        ]

    @override
    def sh(self, imm: Imm, rs1: Register, rs2: Register) -> None:
        self.memory[self.registers[rs1] + imm] = [
            self.registers[rs2] & 0xFF,
            (self.registers[rs2] >> 8) & 0xFF,
        ]

    @override
    def lb(self, imm: Imm, rs1: Register, rd: Register) -> None:
        addr = self.registers[rs1] + imm
        byte = self.memory[addr] & 0xFF

        if byte & 0x80:
            byte |= 0xFFFFFF00

        self.registers[rd] = byte

    @override
    def lbu(self, imm: Imm, rs1: Register, rd: Register) -> None:
        addr = self.registers[rs1] + imm
        self.registers[rd] = self.memory[addr] & 0xFF

    @override
    def lh(self, imm: Imm, rs1: Register, rd: Register) -> None:
        addr = self.registers[rs1] + imm
        hw = self.memory[addr] | (self.memory[addr + 1] << 8)
        hw |= 0xFFFF
        self.registers[rd] = hw

    @override
    def lhu(self, imm: Imm, rs1: Register, rd: Register) -> None:
        addr = self.registers[rs1] + imm
        value = self.memory[addr] | (self.memory[addr + 1] << 8)
        self.registers[rd] = value & 0xFFFF

    @override
    def add(self, rs1: Register, rs2: Register, rd: Register) -> None:
        self.registers[rd] = np.array(self.registers[rs1]) + np.array(self.registers[rs2])

    @override
    def sub(self, rs1: Register, rs2: Register, rd: Register) -> None:
        self.registers[rd] = self.registers[rs1] - self.registers[rs2]

    @override
    def sll(self, rs1: Register, rs2: Register, rd: Register) -> None:
        self.registers[rd] = self.registers[rs1] << (self.registers[rs2] & 0x1F)

    @override
    def slt(self, rs1: Register, rs2: Register, rd: Register) -> None:
        self.registers[rd] = self.registers[rs1] < self.registers[rs2]

    @override
    def sltu(self, rs1: Register, rs2: Register, rd: Register) -> None:
        self.registers[rd] = np.uint32(self.registers[rs1]) < np.uint32(self.registers[rs2])

    @override
    def xor(self, rs1: Register, rs2: Register, rd: Register) -> None:
        self.registers[rd] = self.registers[rs1] ^ self.registers[rs2]

    @override
    def srl(self, rs1: Register, rs2: Register, rd: Register) -> None:
        self.registers[rd] = np.uint32(self.registers[rs1]) >> (self.registers[rs2] & 0x1F)

    @override
    def sra(self, rs1: Register, rs2: Register, rd: Register) -> None:
        value_to_shift = self.registers[rs1]
        shift_amount = self.registers[rs2] & 0x1F

        if value_to_shift & 0x80000000:
            self.registers[rd] = (value_to_shift >> shift_amount) | (0xFFFFFFFF << (32 - shift_amount))

        self.registers[rd] = value_to_shift >> shift_amount

    @override
    def or_(self, rs1: Register, rs2: Register, rd: Register) -> None:
        self.registers[rd] = self.registers[rs1] | self.registers[rs2]

    @override
    def and_(self, rs1: Register, rs2: Register, rd: Register) -> None:
        self.registers[rd] = self.registers[rs1] & self.registers[rs2]

    @override
    def fence(self, rs1: Register, rs2: Register, rd: Register) -> None:
        pass  # Implement as needed

    @override
    def ecall(self, imm: Imm, rs1: Register, rd: Register) -> None:
        sys_call_number = self.registers[17]  # Assuming a0 (x17) holds the system call number
        if sys_call_number == 93:  # exit
            raise SystemExit(self.registers[10])  # Assuming a0 (x10) holds the exit code
        elif sys_call_number == 64:  # print
            addr = self.registers[11]
            while (addr - self.registers[11]) < self.registers[12]:
                print(chr(self.memory[addr]), end="")
                addr += 1

            self.registers[10] = addr - self.registers[11]
        elif sys_call_number == 80:
            self.registers[10] = 0
        elif sys_call_number == 63:
            fd = self.registers[10]
            buf_pointer = self.registers[11]
            count = self.registers[12]

            if fd == 0:
                data = input("")
                data = [ord(char) for char in data]  # type: ignore
                data = data[: min(len(data), count)]
                self.memory[buf_pointer] = data  # type: ignore
                self.registers[10] = len(data)
            else:
                self.registers[10] = -29

        elif sys_call_number == 62:
            self.registers[10] = -29

        elif sys_call_number == 214:
            new_brk = self.registers[10]
            if new_brk == 0:
                self.registers[10] = self.brk
            else:
                self.registers[10] = self.brk = new_brk

        elif sys_call_number == 57:
            self.registers[10] = 0

        else:
            print(f"Unknown syscall {sys_call_number}")
