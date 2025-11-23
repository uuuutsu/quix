from collections.abc import Callable
from functools import wraps
from inspect import signature

from quix.core.interfaces.opcode import OpcodeFactory
from quix.riscv.loader.opcodes import (
    RISCVOpcode,
    add,
    addi,
    and_,
    andi,
    auipc,
    beq,
    bge,
    bgeu,
    blt,
    bltu,
    bne,
    csrrci,
    csrrs,
    csrrsi,
    csrrw,
    csrrwi,
    div,
    divu,
    ecall,
    fence,
    jal,
    jalr,
    lb,
    lbu,
    lh,
    lhu,
    lui,
    lw,
    mul,
    mulh,
    mulhsu,
    mulhu,
    or_,
    ori,
    rem,
    remu,
    sb,
    sh,
    sll,
    slli,
    slt,
    slti,
    sltiu,
    sltu,
    sra,
    srl,
    srli,
    sub,
    sw,
    xor,
    xori,
)

from .decoder import InstructionData
from .opcodes import (
    I_OpCode,
    IJALR_OpCode,
    ILoad_OpCode,
    IMiscMem_OpCode,
    ISystem_OpCode,
    R_OpCode,
    S_OpCode,
    SB_OpCode,
    UAUIPC_OpCode,
    UJ_OpCode,
    ULUI_OpCode,
)


def _create_opcode_from_instr_data[**P, O: RISCVOpcode](opcode: OpcodeFactory[P, O]) -> Callable[[InstructionData], O]:
    params = signature(opcode).parameters

    @wraps(opcode)
    def factory(data: InstructionData) -> O:
        args = {}
        for name, param in params.items():
            if (val := getattr(data, name)) is None:
                raise RuntimeError(f"Required argument {name!r} of instruction {opcode.__name__!r} is None.")

            args[name] = param.annotation(val)
        return opcode(**args)  # type: ignore

    return factory


type Funct3 = int | None
type Funct7 = int | None
type Opcode = int | None

__REGISTRY: dict[tuple[Funct3, Funct7, Opcode], OpcodeFactory[..., RISCVOpcode]] = {
    (0b000, None, I_OpCode): addi,
    (0b010, None, S_OpCode): sw,
    (None, None, UJ_OpCode): jal,
    (0b010, None, ILoad_OpCode): lw,
    (0b111, None, I_OpCode): andi,
    (0b110, None, I_OpCode): ori,
    (0b100, None, I_OpCode): xori,
    (0b001, None, I_OpCode): slli,
    (0b101, None, I_OpCode): srli,
    (0b000, None, SB_OpCode): beq,
    (0b001, None, SB_OpCode): bne,
    (0b100, None, SB_OpCode): blt,
    (0b110, None, SB_OpCode): bltu,
    (0b111, None, SB_OpCode): bgeu,
    (None, None, ULUI_OpCode): lui,
    (0b010, None, I_OpCode): slti,
    (0b011, None, I_OpCode): sltiu,
    (None, None, UAUIPC_OpCode): auipc,
    (0b101, None, SB_OpCode): bge,
    (0b000, None, IJALR_OpCode): jalr,
    (0b000, None, S_OpCode): sb,
    (0b001, None, S_OpCode): sh,
    (0b000, None, ILoad_OpCode): lb,
    (0b100, None, ILoad_OpCode): lbu,
    (0b001, None, ILoad_OpCode): lh,
    (0b101, None, ILoad_OpCode): lhu,
    (0b000, 0b0000000, R_OpCode): add,
    (0b000, 0b0100000, R_OpCode): sub,
    (0b001, 0b0000000, R_OpCode): sll,
    (0b010, 0b0000000, R_OpCode): slt,
    (0b011, 0b0000000, R_OpCode): sltu,
    (0b100, 0b0000000, R_OpCode): xor,
    (0b101, 0b0000000, R_OpCode): srl,
    (0b101, 0b0100000, R_OpCode): sra,
    (0b110, 0b0000000, R_OpCode): or_,
    (0b111, 0b0000000, R_OpCode): and_,
    (0b000, None, IMiscMem_OpCode): fence,
    (0b000, None, ISystem_OpCode): ecall,
    (0b001, None, ISystem_OpCode): csrrw,
    (0b010, None, ISystem_OpCode): csrrs,
    (0b101, None, ISystem_OpCode): csrrwi,
    (0b110, None, ISystem_OpCode): csrrsi,
    (0b111, None, ISystem_OpCode): csrrci,
    (0b000, 0b0000001, R_OpCode): mul,
    (0b001, 0b0000001, R_OpCode): mulh,
    (0b010, 0b0000001, R_OpCode): mulhsu,
    (0b011, 0b0000001, R_OpCode): mulhu,
    (0b100, 0b0000001, R_OpCode): div,
    (0b101, 0b0000001, R_OpCode): divu,
    (0b110, 0b0000001, R_OpCode): rem,
    (0b111, 0b0000001, R_OpCode): remu,
}

REGISTRY: dict[tuple[Funct3, Funct7, Opcode], OpcodeFactory[[InstructionData], RISCVOpcode]] = {
    key: _create_opcode_from_instr_data(opcode) for key, opcode in __REGISTRY.items()
}
