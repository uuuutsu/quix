from typing import Any, Final, Self

from quix.bootstrap.dtypes.const import UCell, UDynamic
from quix.bootstrap.dtypes.unit import Unit
from quix.bootstrap.dtypes.wide import Wide
from quix.bootstrap.macrocodes import (
    add_wide,
    and_unit,
    and_wide,
    assign_unit,
    assign_wide,
    call_eq_wide,
    call_ge_unit,
    call_ge_wide,
    call_ge_wide_signed,
    call_lt_wide,
    call_lt_wide_signed,
    call_neq_wide,
    clear_unit,
    clear_wide,
    div_wide,
    free_wide,
    loop_wide,
    mul_wide,
    not_unit,
    or_wide,
    sub_wide,
    switch_wide,
    xor_wide,
)
from quix.bootstrap.program import SmartProgram, ToConvert, convert
from quix.core.opcodes.dtypes import CoreProgram
from quix.core.opcodes.opcodes import add, inject, output
from quix.exceptions.core.visitor import NoHandlerFoundException
from quix.memoptix.opcodes import free
from quix.riscv.loader.decoder.utils import get_bit_section
from quix.riscv.loader.state import State
from quix.riscv.opcodes.base import RISCVOpcode
from quix.riscv.opcodes.dtypes import Imm, Register

from .runtime import CPU, Layout, Memory
from .utils import is_signed

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


def _strip_data(data: bytes) -> tuple[bytes, int]:
    offset: int = 0
    while data and (data[0] == 0):
        offset += 1
        data = data[1:]
    return data or b"", offset


def _imm_to_const(imm: Imm) -> UDynamic:
    return UDynamic.from_int(imm, 4)


class Compiler:
    __slots__ = (
        "cpu",
        "memory",
        "program",
    )

    def __init__(self) -> None:
        self.cpu = CPU()
        self.memory = Memory()
        self.program = SmartProgram()
        self._init_runtime()

    def run(self, state: State) -> Self:
        self._init_cpu(state)
        self._init_registers(state)
        self._init_memory(state)
        self._compile_exec_loop(state)
        return self

    def _init_runtime(self) -> None:
        self.program |= Layout().add_component(self.cpu, 0).add_component(self.memory, 0).create(50)

    def _init_cpu(self, state: State) -> None:
        self.program |= self.cpu.set_pc(UDynamic.from_int(state.entry, size=4))

    def _init_memory(self, state: State) -> None:
        for name in _DATA_SECTIONS:
            if section := state.sections.get(name):
                data, offset = _strip_data(section.data())  # type: ignore
                if not data:
                    continue
                self.program |= self.memory.store(
                    UDynamic.from_int(section.header["sh_addr"] + offset),
                    UDynamic.from_bytes(data),
                )

    def _init_registers(self, state: State) -> None:
        self.program |= self.cpu.store_register(
            UDynamic.from_int(1),
            UDynamic.from_int(max(state.code) + 4),
        )
        self.program |= self.cpu.store_register(
            UDynamic.from_int(2),
            UDynamic.from_int(16000),
        )
        if sbss := state.sections.get(".sbss"):
            self.program |= self.cpu.store_register(
                UDynamic.from_int(3),
                UDynamic.from_int(sbss.header["sh_addr"] + 2048),
            )
        self.program |= self.cpu.store_register(
            UDynamic.from_int(8),
            UDynamic.from_int(4048),
        )

    def _compile_exec_loop(self, state: State) -> None:
        mapping: dict[UDynamic, CoreProgram] = {}
        total = len(state.code)
        for idx, (index, riscv_opcode) in enumerate(state.code.items()):
            mapping[UDynamic.from_int(index, 4)] = self._execute(riscv_opcode)
            print(f"instruction compiled: {idx}/{total - 1}")

        self.program |= self.cpu.run(mapping)

    @convert
    def _execute(self, opcode: RISCVOpcode) -> ToConvert:
        new_args: dict[str, Any] = {}
        rs_mapping: dict[Register, Wide] = {}

        for name, value in opcode.args().items():
            if isinstance(value, Imm):
                new_args[name] = _imm_to_const(value)
            elif isinstance(value, Register):
                rs_mapping[value] = buff = Wide.from_length(f"{name}_buff", 4)
                new_args[name] = buff
                yield self.cpu.load_register(UDynamic.from_int(value), buff)
            else:
                raise ValueError(f"Unknown argument type: {type(value)}")

        if custom_handler := getattr(self, opcode.__id__, None):
            yield custom_handler(**new_args)
        else:
            raise NoHandlerFoundException(opcode, self)

        for index, from_ in rs_mapping.items():
            yield self.cpu.store_register(UDynamic.from_int(index), from_)
            yield clear_wide(from_)
            yield free_wide(from_)

        return inject(None, "!", None)

    def addi(self, imm: UDynamic, rs1: Wide, rd: Wide) -> ToConvert:
        if is_signed(imm):
            yield sub_wide(rs1, imm, rd)
        else:
            yield add_wide(rs1, imm, rd)
        return self.cpu.next()

    def sw(self, imm: UDynamic, rs1: Wide, rs2: Wide) -> ToConvert:
        yield add_wide(rs1, imm, rs1)
        yield self.memory.store(rs1, rs2)
        return self.cpu.next()

    def jal(self, imm: UDynamic, rd: Wide) -> ToConvert:
        yield assign_wide(rd, self.cpu.pc)
        yield add_wide(rd, UDynamic.from_int(4, 4), rd)
        return add_wide(self.cpu.pc, imm, self.cpu.pc)

    def lw(self, imm: UDynamic, rs1: Wide, rd: Wide) -> ToConvert:
        yield add_wide(imm, rs1, rs1)
        yield self.memory.load(rs1, rd)
        return self.cpu.next()

    def andi(self, imm: UDynamic, rs1: Wide, rd: Wide) -> ToConvert:
        yield assign_wide(rd, imm)
        yield and_wide(rs1, rd, rd)
        return self.cpu.next()

    def ori(self, imm: UDynamic, rs1: Wide, rd: Wide) -> ToConvert:
        yield assign_wide(rd, imm)
        yield or_wide(rs1, rd, rd)
        return self.cpu.next()

    def xori(self, imm: UDynamic, rs1: Wide, rd: Wide) -> ToConvert:
        yield assign_wide(rd, imm)
        yield xor_wide(rs1, rd, rd)
        return self.cpu.next()

    def slli(self, imm: UDynamic, rs1: Wide, rd: Wide) -> ToConvert:
        # SIGNED ARE NOT YET HANDLED
        yield mul_wide(rs1, UDynamic.from_int(2 ** (int(imm) & 0x1F), 4), rd)
        return self.cpu.next()

    def srli(self, imm: UDynamic, rs1: Wide, rd: Wide) -> ToConvert:
        # SIGNED ARE NOT YET HANDLED
        if get_bit_section(int(imm), 10, 10):
            yield div_wide(
                rs1,
                UDynamic.from_int(2 ** (int(imm) & 0x1F), 4),
                quotient=rd,
                remainder=None,
            )
        else:
            yield div_wide(
                rs1,
                UDynamic.from_int(2 ** (int(imm) & 0x1F), 4),
                quotient=rd,
                remainder=None,
            )
        return self.cpu.next()

    def beq(self, imm: UDynamic, rs1: Wide, rs2: Wide) -> ToConvert:
        return call_eq_wide(
            rs1,
            rs2,
            add_wide(self.cpu.pc, imm, self.cpu.pc),
            [],
        )

    def bne(self, imm: UDynamic, rs1: Wide, rs2: Wide) -> ToConvert:
        return call_neq_wide(
            rs1,
            rs2,
            add_wide(self.cpu.pc, imm, self.cpu.pc),
            [],
        )

    def bge(self, imm: UDynamic, rs1: Wide, rs2: Wide) -> ToConvert:
        return call_ge_wide_signed(
            rs1,
            rs2,
            add_wide(self.cpu.pc, imm, self.cpu.pc),
            [],
        )

    def blt(self, imm: UDynamic, rs1: Wide, rs2: Wide) -> ToConvert:
        return call_lt_wide_signed(
            rs1,
            rs2,
            add_wide(self.cpu.pc, imm, self.cpu.pc),
            [],
        )

    def bltu(self, imm: UDynamic, rs1: Wide, rs2: Wide) -> ToConvert:
        return call_lt_wide(
            rs1,
            rs2,
            add_wide(self.cpu.pc, imm, self.cpu.pc),
            [],
        )

    def bgeu(self, imm: UDynamic, rs1: Wide, rs2: Wide) -> ToConvert:
        return call_ge_wide(
            rs1,
            rs2,
            add_wide(self.cpu.pc, imm, self.cpu.pc),
            [],
        )

    def lui(self, imm: UDynamic, rd: Wide) -> ToConvert:
        yield assign_wide(rd, imm)
        return self.cpu.next()

    def slti(self, imm: UDynamic, rs1: Wide, rd: Wide) -> ToConvert:
        imm_wide = Wide.from_length("imm", 4)
        yield assign_wide(imm_wide, imm)
        yield call_lt_wide_signed(
            rs1,
            imm_wide,
            assign_wide(rd, UDynamic.from_int(1, 4)),
            assign_wide(rd, UDynamic.from_int(1, 4)),
        )
        yield clear_wide(imm_wide), free_wide(imm_wide)
        return self.cpu.next()

    def sltiu(self, imm: UDynamic, rs1: Wide, rd: Wide) -> ToConvert:
        imm_wide = Wide.from_length("imm", 4)
        yield assign_wide(imm_wide, imm)
        yield call_lt_wide(
            rs1,
            imm_wide,
            assign_wide(rd, UDynamic.from_int(1, 4)),
            assign_wide(rd, UDynamic.from_int(1, 4)),
        )
        yield clear_wide(imm_wide), free_wide(imm_wide)
        return self.cpu.next()

    def auipc(self, imm: UDynamic, rd: Wide) -> ToConvert:
        return add_wide(self.cpu.pc, imm, rd)

    def jalr(self, imm: UDynamic, rs1: Wide, rd: Wide) -> ToConvert:
        yield assign_wide(rd, self.cpu.pc)
        yield add_wide(rd, UDynamic.from_int(4, 4), rd)
        yield assign_wide(self.cpu.pc, rs1)
        yield add_wide(self.cpu.pc, imm, self.cpu.pc)
        mask = Unit("mask")
        yield assign_unit(mask, UCell.from_value(0b11111110))
        yield and_unit(self.cpu.pc[0], mask, self.cpu.pc[0])
        yield add(mask, 2)  # to zero
        return free(mask)

    def sb(self, imm: UDynamic, rs1: Wide, rs2: Wide) -> ToConvert:
        yield add_wide(rs1, imm, rs1)
        yield self.memory.store(rs1, Wide("lsb", (rs2[0],)))
        return self.cpu.next()

    def sh(self, imm: UDynamic, rs1: Wide, rs2: Wide) -> ToConvert:
        yield add_wide(rs1, imm, rs1)
        yield self.memory.store(rs1, Wide("half", rs2[:2]))
        return self.cpu.next()

    def lb(self, imm: UDynamic, rs1: Wide, rd: Wide) -> ToConvert:
        yield add_wide(imm, rs1, rs1)
        yield clear_wide(Wide("rd_upper", rd[1:]))
        yield self.memory.load(rs1, Wide("lsb", (rd[0],)))
        lim = Unit("lim")
        yield assign_unit(lim, UCell.from_value(128))
        yield call_ge_unit(
            rd[0],
            lim,
            [add(rd[1], -1), add(rd[2], -1), add(rd[3], -1), *not_unit(rd[0], rd[0])],
            [],
        )
        yield clear_unit(lim), free(lim)
        return self.cpu.next()

    def lbu(self, imm: UDynamic, rs1: Wide, rd: Wide) -> ToConvert:
        yield add_wide(imm, rs1, rs1)
        yield clear_wide(Wide("rd_upper", rd[1:]))
        yield self.memory.load(rs1, Wide("lsb", (rd[0],)))
        return self.cpu.next()

    def lh(self, imm: UDynamic, rs1: Wide, rd: Wide) -> ToConvert:
        yield add_wide(imm, rs1, rs1)
        yield clear_wide(Wide("rd_upper", rd[2:]))
        yield self.memory.load(rs1, Wide("lsb", rd[:2]))
        lim = Unit("lim")
        yield assign_unit(lim, UCell.from_value(128))
        yield call_ge_unit(
            rd[1],
            lim,
            [add(rd[2], -1), add(rd[3], -1), *not_unit(rd[0], rd[0]), *not_unit(rd[1], rd[1])],
            [],
        )
        yield clear_unit(lim), free(lim)
        return self.cpu.next()

    def lhu(self, imm: UDynamic, rs1: Wide, rd: Wide) -> ToConvert:
        yield add_wide(imm, rs1, rs1)
        yield clear_wide(Wide("rd_upper", rd[2:]))
        yield self.memory.load(rs1, Wide("lsb", rd[:2]))
        return self.cpu.next()

    def add(self, rs1: Wide, rs2: Wide, rd: Wide) -> ToConvert:
        yield add_wide(rs1, rs2, rd)
        return self.cpu.next()

    def sub(self, rs1: Wide, rs2: Wide, rd: Wide) -> ToConvert:
        yield sub_wide(rs1, rs2, rd)
        return self.cpu.next()

    def sll(self, rs1: Wide, rs2: Wide, rd: Wide) -> ToConvert:
        yield mul_wide(UDynamic.from_int(2, 4), rs2, rs2)
        yield mul_wide(rs1, rs2, rd)
        return self.cpu.next()

    def slt(self, rs1: Wide, rs2: Wide, rd: Wide) -> ToConvert:
        yield call_lt_wide_signed(
            rs1,
            rs2,
            assign_wide(rd, UDynamic.from_int(1, 4)),
            assign_wide(rd, UDynamic.from_int(1, 4)),
        )
        return self.cpu.next()

    def sltu(self, rs1: Wide, rs2: Wide, rd: Wide) -> ToConvert:
        yield call_lt_wide(
            rs1,
            rs2,
            assign_wide(rd, UDynamic.from_int(1, 4)),
            assign_wide(rd, UDynamic.from_int(1, 4)),
        )
        return self.cpu.next()

    def xor(self, rs1: Wide, rs2: Wide, rd: Wide) -> ToConvert:
        yield xor_wide(rs1, rs2, rd)
        return self.cpu.next()

    def or_(self, rs1: Wide, rs2: Wide, rd: Wide) -> ToConvert:
        yield or_wide(rs1, rs2, rd)
        return self.cpu.next()

    def and_(self, rs1: Wide, rs2: Wide, rd: Wide) -> ToConvert:
        yield and_wide(rs1, rs2, rd)
        return self.cpu.next()

    def fence(self, rs1: Wide, rs2: Wide, rd: Wide) -> ToConvert:
        pass  # Implement as needed

    def srl(self, rs1: Wide, rs2: Wide, rd: Wide) -> ToConvert:
        # SIGNED ARE NOT YET HANDLED
        yield mul_wide(UDynamic.from_int(2, 4), rs2, rs2)
        yield div_wide(
            rs1,
            rs2,
            quotient=rd,
            remainder=None,
        )
        return self.cpu.next()

    def sra(self, rs1: Wide, rs2: Wide, rd: Wide) -> ToConvert:
        # SIGNED ARE NOT YET HANDLED
        yield mul_wide(UDynamic.from_int(2, 4), rs2, rs2)
        yield div_wide(
            rs1,
            rs2,
            quotient=rd,
            remainder=None,
        )
        return self.cpu.next()

    def ecall(self, imm: UDynamic, rs1: Wide, rd: Wide) -> ToConvert:
        cases: dict[UDynamic, CoreProgram] = {
            UDynamic.from_int(62, 1): self._ecall_lseek(),
            UDynamic.from_int(64, 1): self._ecall_print(),
            UDynamic.from_int(57, 1): self._ecall_close(),
            UDynamic.from_int(93, 1): self._ecall_exit(),
            UDynamic.from_int(10, 1): [],
        }

        x17 = Wide.from_length("x17", 1)
        yield self.memory.load(UDynamic.from_int(17), x17)
        yield switch_wide(x17, cases, [])

        yield clear_wide(x17), free_wide(x17)
        return self.cpu.next()

    @convert
    def _ecall_close(self) -> ToConvert:
        return self.memory.store(UDynamic.from_int(10), UDynamic.from_int(0, 4))

    @convert
    def _ecall_lseek(self) -> ToConvert:
        return self.memory.store(UDynamic.from_int(10), UDynamic.from_int((1 << 32) - 29))

    @convert
    def _ecall_exit(self) -> ToConvert:
        return clear_unit(self.cpu.exit)

    @convert
    def _ecall_print(self) -> ToConvert:
        addr = Wide.from_length("addr", 4)
        counter = Wide.from_length("counter", 4)
        yield self.cpu.load_register(UDynamic.from_int(11), addr)
        yield self.cpu.load_register(UDynamic.from_int(12), counter)

        char = Unit("char")
        yield loop_wide(
            counter,
            self.memory.load(addr, Wide("char", (char,)))
            | output(char)
            | clear_unit(char)
            | add_wide(addr, UDynamic.from_int(1, 4), addr)
            | sub_wide(counter, UDynamic.from_int(1, 4), counter),
        )

        # TODO: set x10 to length of written text
        yield clear_wide(addr), clear_wide(counter)
        return free_wide(addr), free_wide(counter)

    def rem(self, **kwargs: Any) -> ToConvert:
        return self.cpu.next()

    def remu(self, **kwargs: Any) -> ToConvert:
        return self.cpu.next()
