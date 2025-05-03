from abc import abstractmethod

from quix.riscv.decompiler import State
from quix.riscv.opcodes import Imm, Register


class RISCVExecutor:
    __slots__ = ()

    def run(self, state: State) -> None:
        raise NotImplementedError

    @abstractmethod
    def addi(self, imm: Imm, rs1: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def sw(self, imm: Imm, rs1: Register, rs2: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def jal(self, imm: Imm, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def lw(self, imm: Imm, rs1: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def andi(self, imm: Imm, rs1: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def ori(self, imm: Imm, rs1: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def xori(self, imm: Imm, rs1: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def slli(self, imm: Imm, rs1: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def srli(self, imm: Imm, rs1: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def beq(self, imm: Imm, rs1: Register, rs2: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def bne(self, imm: Imm, rs1: Register, rs2: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def blt(self, imm: Imm, rs1: Register, rs2: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def bltu(self, imm: Imm, rs1: Register, rs2: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def bgeu(self, imm: Imm, rs1: Register, rs2: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def lui(self, imm: Imm, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def slti(self, imm: Imm, rs1: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def sltiu(self, imm: Imm, rs1: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def auipc(self, imm: Imm, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def bge(self, imm: Imm, rs1: Register, rs2: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def jalr(self, imm: Imm, rs1: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def sb(self, imm: Imm, rs1: Register, rs2: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def sh(self, imm: Imm, rs1: Register, rs2: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def lb(self, imm: Imm, rs1: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def lbu(self, imm: Imm, rs1: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def lh(self, imm: Imm, rs1: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def lhu(self, imm: Imm, rs1: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def add(self, rs1: Register, rs2: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def sub(self, rs1: Register, rs2: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def sll(self, rs1: Register, rs2: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def slt(self, rs1: Register, rs2: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def sltu(self, rs1: Register, rs2: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def xor(self, rs1: Register, rs2: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def srl(self, rs1: Register, rs2: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def sra(self, rs1: Register, rs2: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def or_(self, rs1: Register, rs2: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def and_(self, rs1: Register, rs2: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def fence(self, rs1: Register, rs2: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def ecall(self, imm: Imm, rs1: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def csrrw(self, imm: Imm, rs1: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def csrrs(self, imm: Imm, rs1: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def csrrwi(self, imm: Imm, rs1: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def csrrsi(self, imm: Imm, rs1: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def csrrci(self, imm: Imm, rs1: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def mul(self, rs1: Register, rs2: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def mulh(self, rs1: Register, rs2: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def mulhsu(self, rs1: Register, rs2: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def mulhu(self, rs1: Register, rs2: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def div(self, rs1: Register, rs2: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def divu(self, rs1: Register, rs2: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def rem(self, rs1: Register, rs2: Register, rd: Register) -> None:
        raise NotImplementedError

    @abstractmethod
    def remu(self, rs1: Register, rs2: Register, rd: Register) -> None:
        raise NotImplementedError
