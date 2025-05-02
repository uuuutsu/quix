__all__ = ("decode",)

from quix.riscv.opcodes.base import RISCVOpcode


def decode(instr: bytes) -> RISCVOpcode:
    raise NotImplementedError
