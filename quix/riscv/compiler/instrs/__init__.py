from typing import Any

from .add import riscv_add
from .addi import riscv_addi
from .and_ import riscv_and_
from .andi import riscv_andi
from .auipc import riscv_auipc
from .beq import riscv_beq
from .bge import riscv_bge
from .bgeu import riscv_bgeu
from .blt import riscv_blt
from .bltu import riscv_bltu
from .bne import riscv_bne
from .ecall import riscv_ecall
from .fence import riscv_fence
from .jal import riscv_jal
from .jalr import riscv_jalr
from .lb import riscv_lb
from .lbu import riscv_lbu
from .lh import riscv_lh
from .lhu import riscv_lhu
from .lui import riscv_lui
from .lw import riscv_lw
from .or_ import riscv_or_
from .ori import riscv_ori
from .rem import riscv_rem
from .remu import riscv_remu
from .sb import riscv_sb
from .sh import riscv_sh
from .sll import riscv_sll
from .slli import riscv_slli
from .slt import riscv_slt
from .slti import riscv_slti
from .sltiu import riscv_sltiu
from .sltu import riscv_sltu
from .sra import riscv_sra
from .srl import riscv_srl
from .srli import riscv_srli
from .sub import riscv_sub
from .sw import riscv_sw
from .utils import is_signed
from .xor import riscv_xor
from .xori import riscv_xori

__all__ = (
    "get_instr",
    "is_signed",
    "riscv_add",
    "riscv_addi",
    "riscv_and_",
    "riscv_andi",
    "riscv_auipc",
    "riscv_beq",
    "riscv_bge",
    "riscv_bgeu",
    "riscv_blt",
    "riscv_bltu",
    "riscv_bne",
    "riscv_ecall",
    "riscv_fence",
    "riscv_jal",
    "riscv_jalr",
    "riscv_lb",
    "riscv_lbu",
    "riscv_lh",
    "riscv_lhu",
    "riscv_lui",
    "riscv_lw",
    "riscv_or_",
    "riscv_ori",
    "riscv_rem",
    "riscv_remu",
    "riscv_sb",
    "riscv_sh",
    "riscv_sll",
    "riscv_slli",
    "riscv_slt",
    "riscv_slti",
    "riscv_sltiu",
    "riscv_sltu",
    "riscv_sra",
    "riscv_srl",
    "riscv_srli",
    "riscv_sub",
    "riscv_sw",
    "riscv_xor",
    "riscv_xori",
)


def get_instr(name: str) -> Any:
    prefixed_name = f"riscv_{name}"
    instr = globals().get(prefixed_name)
    if instr is None:
        raise KeyError(f"Instruction '{name}' not found (looked for '{prefixed_name}')")
    return instr
