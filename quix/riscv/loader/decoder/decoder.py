from dataclasses import dataclass

from .section import (
    B_Imm,
    BaseSection,
    I_Imm,
    J_Imm,
    S_Imm,
    Section,
    U_Imm,
)


@dataclass(slots=True)
class InstructionData:
    rs1: int | None = None
    rs2: int | None = None
    rd: int | None = None
    imm: int | None = None
    funct3: int | None = None
    funct7: int | None = None
    opcode: int | None = None


@dataclass(slots=True)
class Decoder:
    rs1: BaseSection | None = None
    rs2: BaseSection | None = None
    rd: BaseSection | None = None
    imm: BaseSection | None = None
    funct3: BaseSection | None = None
    funct7: BaseSection | None = None

    def decode(self, instr: int) -> InstructionData:
        data = {"opcode": self.get_opcode(instr)}

        for field in self.__slots__:
            if (sec := getattr(self, field)) is None:
                continue

            data[field] = sec.decode(instr)

        return InstructionData(**data)

    @staticmethod
    def get_opcode(instr: int) -> int:
        return instr & 0x7F


R_Decoder = Decoder(
    funct7=Section(31, 25),
    rs2=Section(24, 20),
    rs1=Section(19, 15),
    funct3=Section(14, 12),
    rd=Section(11, 7),
)
I_Decoder = Decoder(
    rs1=Section(19, 15),
    funct3=Section(14, 12),
    rd=Section(11, 7),
    imm=I_Imm,
)

ILoad_Decoder = Decoder(
    rs1=Section(19, 15),
    funct3=Section(14, 12),
    rd=Section(11, 7),
    imm=I_Imm,
)

IJALR_Decoder = Decoder(
    rs1=Section(19, 15),
    funct3=Section(14, 12),
    rd=Section(11, 7),
    imm=I_Imm,
)

S_Decoder = Decoder(
    rs2=Section(24, 20),
    rs1=Section(19, 15),
    funct3=Section(14, 12),
    imm=S_Imm,
)

SB_Decoder = Decoder(
    rs2=Section(24, 20),
    rs1=Section(19, 15),
    funct3=Section(14, 12),
    imm=B_Imm,
)

ULUI_Decoder = Decoder(
    rd=Section(11, 7),
    imm=U_Imm,
)

UAUIPC_Decoder = Decoder(
    rd=Section(11, 7),
    imm=U_Imm,
)

UJ_Decoder = Decoder(
    rd=Section(11, 7),
    imm=J_Imm,
)
