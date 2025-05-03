from typing import Final, override

from quix.riscv.executors.base import RISCVExecutor
from quix.riscv.loader import State
from quix.riscv.opcodes import Imm, Register

from .memory import EmuMemory

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
    __slots__ = (
        "memory",
        "registers",
        "pc",
        "csr",
    )

    def __init__(self) -> None:
        self.registers = [0] * 32
        self.memory = EmuMemory()
        self.pc = 0
        self.csr: dict[int, int] = {}

    @override
    def run(self, state: State) -> None:
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
                exit()

            if prev_pc == self.pc:
                self.pc += 4
            self.registers[0] = 0

    @override
    def addi(self, imm: Imm, rs1: Register, rd: Register) -> None:
        self.registers[rd] = self.registers[rs1] + imm

    @override
    def sw(self, imm: Imm, rs1: Register, rs2: Register) -> None:
        self.memory[self.registers[rs1] + imm] = self.registers[rs2]

    @override
    def jal(self, imm: Imm, rd: Register) -> None:
        self.registers[rd] = self.pc + 4
        self.pc += imm

    @override
    def lw(self, imm: Imm, rs1: Register, rd: Register) -> None:
        base_addr = self.registers[rs1] + imm
        self.registers[rd] = self.memory.get_word(base_addr)

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
        self.registers[rd] = self.registers[rs1] << imm

    @override
    def srli(self, imm: Imm, rs1: Register, rd: Register) -> None:
        if (imm >> 6) > 0:
            value_to_shift = self.registers[rs1]

            if value_to_shift & 0x80000000:
                self.registers[rd] = (value_to_shift >> imm) | (0xFFFFFFFF << (32 - imm))

            self.registers[rd] = value_to_shift >> imm
            return

        self.registers[rd] = self.registers[rs1] >> imm

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
        if self.registers[rs1] < self.registers[rs2]:
            self.pc += imm

    @override
    def bgeu(self, imm: Imm, rs1: Register, rs2: Register) -> None:
        if self.registers[rs1] >= self.registers[rs2]:
            self.pc += imm

    @override
    def lui(self, imm: Imm, rd: Register) -> None:
        self.registers[rd] = imm

    @override
    def slti(self, imm: Imm, rs1: Register, rd: Register) -> None:
        self.registers[rd] = self.registers[rs1] < imm

    @override
    def sltiu(self, imm: Imm, rs1: Register, rd: Register) -> None:
        self.registers[rd] = (self.registers[rs1] & 0xFFFFFFFF) < (imm & 0xFFFFFFFF)

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
        self.pc = (self.registers[rs1] + imm) & ~1
        self.registers[rd] = temp + 4

    @override
    def sb(self, imm: Imm, rs1: Register, rs2: Register) -> None:
        addr = self.registers[rs1] + imm
        self.memory[addr] = self.registers[rs2] & 0xFF

    @override
    def sh(self, imm: Imm, rs1: Register, rs2: Register) -> None:
        addr = self.registers[rs1] + imm
        self.memory[addr] = self.registers[rs2] & 0xFFFF

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
        self.registers[rd] = self.registers[rs1] + self.registers[rs2]

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
        self.registers[rd] = (self.registers[rs1] & 0xFFFFFFFF) < (self.registers[rs2] & 0xFFFFFFFF)

    @override
    def xor(self, rs1: Register, rs2: Register, rd: Register) -> None:
        self.registers[rd] = self.registers[rs1] ^ self.registers[rs2]

    @override
    def srl(self, rs1: Register, rs2: Register, rd: Register) -> None:
        self.registers[rd] = self.registers[rs1] >> (self.registers[rs2] & 0x1F)

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
        if imm > 0:
            exit()
        # Implement syscall handling

    @override
    def csrrw(self, imm: Imm, rs1: Register, rd: Register) -> None:
        old_value = self.csr.get(imm, 0)
        self.csr[imm] = self.registers[rs1]
        self.registers[rd] = old_value

    @override
    def csrrs(self, imm: Imm, rs1: Register, rd: Register) -> None:
        old_value = self.csr.get(imm, 0)
        self.csr[imm] = old_value | self.registers[rs1]
        self.registers[rd] = old_value

    @override
    def csrrwi(self, imm: Imm, rs1: Register, rd: Register) -> None:
        old_value = self.csr.get(imm, 0)
        self.csr[imm] = rs1
        self.registers[rd] = old_value

    @override
    def csrrsi(self, imm: Imm, rs1: Register, rd: Register) -> None:
        old_value = self.csr.get(imm, 0)
        self.csr[imm] = old_value | rs1
        self.registers[rd] = old_value

    @override
    def csrrci(self, imm: Imm, rs1: Register, rd: Register) -> None:
        old_value = self.csr.get(imm, 0)
        self.csr[imm] = old_value & ~rs1
        self.registers[rd] = old_value

    @override
    def mul(self, rs1: Register, rs2: Register, rd: Register) -> None:
        self.registers[rd] = self.registers[rs1] * self.registers[rs2]

    @override
    def mulh(self, rs1: Register, rs2: Register, rd: Register) -> None:
        result = (self.registers[rs1] * self.registers[rs2]) >> 32
        self.registers[rd] = result & 0xFFFFFFFF

    @override
    def mulhsu(self, rs1: Register, rs2: Register, rd: Register) -> None:
        result = (self.registers[rs1] * self.registers[rs2]) >> 32
        self.registers[rd] = result & 0xFFFFFFFF

    @override
    def mulhu(self, rs1: Register, rs2: Register, rd: Register) -> None:
        result = (self.registers[rs1] * self.registers[rs2]) >> 32
        self.registers[rd] = result & 0xFFFFFFFF

    @override
    def div(self, rs1: Register, rs2: Register, rd: Register) -> None:
        self.registers[rd] = self.registers[rs1] // self.registers[rs2] if self.registers[rs2] != 0 else -1

    @override
    def divu(self, rs1: Register, rs2: Register, rd: Register) -> None:
        self.registers[rd] = (
            (self.registers[rs1] & 0xFFFFFFFF) // (self.registers[rs2] & 0xFFFFFFFF)
            if self.registers[rs2] != 0
            else 0xFFFFFFFF
        )

    @override
    def rem(self, rs1: Register, rs2: Register, rd: Register) -> None:
        self.registers[rd] = (
            self.registers[rs1] % self.registers[rs2] if self.registers[rs2] != 0 else self.registers[rs1]
        )

    @override
    def remu(self, rs1: Register, rs2: Register, rd: Register) -> None:
        self.registers[rd] = (
            (self.registers[rs1] & 0xFFFFFFFF) % (self.registers[rs2] & 0xFFFFFFFF)
            if self.registers[rs2] != 0
            else self.registers[rs1] & 0xFFFFFFFF
        )
