from .base import opcode
from .dtypes import Imm, Register


@opcode
def addi(imm: Imm, rs1: Register, rd: Register) -> None: ...


@opcode
def sw(imm: Imm, rs1: Register, rs2: Register) -> None: ...


@opcode
def jal(imm: Imm, rd: Register) -> None: ...


@opcode
def lw(imm: Imm, rs1: Register, rd: Register) -> None: ...


@opcode
def andi(imm: Imm, rs1: Register, rd: Register) -> None: ...


@opcode
def ori(imm: Imm, rs1: Register, rd: Register) -> None: ...


@opcode
def xori(imm: Imm, rs1: Register, rd: Register) -> None: ...


@opcode
def slli(imm: Imm, rs1: Register, rd: Register) -> None: ...


@opcode
def srli(imm: Imm, rs1: Register, rd: Register) -> None: ...


@opcode
def beq(imm: Imm, rs1: Register, rs2: Register) -> None: ...


@opcode
def bne(imm: Imm, rs1: Register, rs2: Register) -> None: ...


@opcode
def blt(imm: Imm, rs1: Register, rs2: Register) -> None: ...


@opcode
def bltu(imm: Imm, rs1: Register, rs2: Register) -> None: ...


@opcode
def bgeu(imm: Imm, rs1: Register, rs2: Register) -> None: ...


@opcode
def lui(imm: Imm, rd: Register) -> None: ...


@opcode
def slti(imm: Imm, rs1: Register, rd: Register) -> None: ...


@opcode
def sltiu(imm: Imm, rs1: Register, rd: Register) -> None: ...


@opcode
def auipc(imm: Imm, rd: Register) -> None: ...


@opcode
def bge(imm: Imm, rs1: Register, rs2: Register) -> None: ...


@opcode
def jalr(imm: Imm, rs1: Register, rd: Register) -> None: ...


@opcode
def sb(imm: Imm, rs1: Register, rs2: Register) -> None: ...


@opcode
def sh(imm: Imm, rs1: Register, rs2: Register) -> None: ...


@opcode
def lb(imm: Imm, rs1: Register, rd: Register) -> None: ...


@opcode
def lbu(imm: Imm, rs1: Register, rd: Register) -> None: ...


@opcode
def lh(imm: Imm, rs1: Register, rd: Register) -> None: ...


@opcode
def lhu(imm: Imm, rs1: Register, rd: Register) -> None: ...


@opcode
def add(rs1: Register, rs2: Register, rd: Register) -> None: ...


@opcode
def sub(rs1: Register, rs2: Register, rd: Register) -> None: ...


@opcode
def sll(rs1: Register, rs2: Register, rd: Register) -> None: ...


@opcode
def slt(rs1: Register, rs2: Register, rd: Register) -> None: ...


@opcode
def sltu(rs1: Register, rs2: Register, rd: Register) -> None: ...


@opcode
def xor(rs1: Register, rs2: Register, rd: Register) -> None: ...


@opcode
def srl(rs1: Register, rs2: Register, rd: Register) -> None: ...


@opcode
def sra(rs1: Register, rs2: Register, rd: Register) -> None: ...


@opcode
def or_(rs1: Register, rs2: Register, rd: Register) -> None: ...


@opcode
def and_(rs1: Register, rs2: Register, rd: Register) -> None: ...


@opcode
def fence(rs1: Register, rs2: Register, rd: Register) -> None: ...


@opcode
def ecall(imm: Imm, rs1: Register, rd: Register) -> None: ...


@opcode
def csrrw(imm: Imm, rs1: Register, rd: Register) -> None: ...


@opcode
def csrrs(imm: Imm, rs1: Register, rd: Register) -> None: ...


@opcode
def csrrwi(imm: Imm, rs1: Register, rd: Register) -> None: ...


@opcode
def csrrsi(imm: Imm, rs1: Register, rd: Register) -> None: ...


@opcode
def csrrci(imm: Imm, rs1: Register, rd: Register) -> None: ...


@opcode
def mul(rs1: Register, rs2: Register, rd: Register) -> None: ...


@opcode
def mulh(rs1: Register, rs2: Register, rd: Register) -> None: ...


@opcode
def mulhsu(rs1: Register, rs2: Register, rd: Register) -> None: ...


@opcode
def mulhu(rs1: Register, rs2: Register, rd: Register) -> None: ...


@opcode
def div(rs1: Register, rs2: Register, rd: Register) -> None: ...


@opcode
def divu(rs1: Register, rs2: Register, rd: Register) -> None: ...


@opcode
def rem(rs1: Register, rs2: Register, rd: Register) -> None: ...


@opcode
def remu(rs1: Register, rs2: Register, rd: Register) -> None: ...
