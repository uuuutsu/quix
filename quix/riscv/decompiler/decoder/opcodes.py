from .decoder import (
    Decoder,
    I_Decoder,
    IJALR_Decoder,
    ILoad_Decoder,
    R_Decoder,
    S_Decoder,
    SB_Decoder,
    UAUIPC_Decoder,
    UJ_Decoder,
    ULUI_Decoder,
)

R_OpCode = 0b0110011
I_OpCode = 0b0010011
IMiscMem_OpCode = 0b0000011
ISystem_OpCode = 0b1110011
ILoad_OpCode = 0b0000011
IJALR_OpCode = 0b1100111
S_OpCode = 0b0100011
SB_OpCode = 0b1100011
ULUI_OpCode = 0b0110111
UAUIPC_OpCode = 0b0010111
UJ_OpCode = 0b1101111


OpCode_To_Decoder: dict[int, Decoder] = {
    R_OpCode: R_Decoder,
    I_OpCode: I_Decoder,
    ILoad_OpCode: ILoad_Decoder,
    IJALR_OpCode: IJALR_Decoder,
    S_OpCode: S_Decoder,
    SB_OpCode: SB_Decoder,
    ULUI_OpCode: ULUI_Decoder,
    UAUIPC_OpCode: UAUIPC_Decoder,
    UJ_OpCode: UJ_Decoder,
    ISystem_OpCode: I_Decoder,
    IMiscMem_OpCode: I_Decoder,
}


OP_BIT_LENGTH = 32
