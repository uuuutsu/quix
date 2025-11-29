from quix.riscv.loader.opcodes import RISCVOpcode

from .decoder import Decoder
from .opcodes import OpCode_To_Decoder
from .registry import REGISTRY


def decode(instr: int) -> RISCVOpcode:
    opcode_id = Decoder.get_opcode(instr)
    try:
        decoder = OpCode_To_Decoder[opcode_id]
    except KeyError as e:
        raise ValueError(f"Invalid opcode: {opcode_id}") from e

    data = decoder.decode(instr)
    opcode = REGISTRY[(data.funct3, data.funct7, data.opcode)]
    return opcode(data)
