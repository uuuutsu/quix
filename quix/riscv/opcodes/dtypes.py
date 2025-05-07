__all__ = (
    "Register",
    "RISCVProgram",
    "Imm",
)


from quix.core.interfaces import Program

from .base import RISCVOpcode

type RISCVProgram = Program[RISCVOpcode]


class Imm(int): ...


class Register(int): ...
