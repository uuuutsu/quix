from quix.bootstrap.dtypes.array import Array
from quix.bootstrap.dtypes.const import UDynamic
from quix.bootstrap.dtypes.unit import Unit
from quix.bootstrap.dtypes.wide import Wide
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.macrocodes import (
    add_wide,
    clear_unit,
    clear_wide,
    free_wide,
    load_array,
    loop_wide,
    store_array,
    sub_wide,
    switch_wide,
)
from quix.bootstrap.macrocodes.nop import NOP
from quix.bootstrap.program import ToConvert
from quix.core.opcodes.base import CoreOpcode
from quix.core.opcodes.opcodes import output


@macrocode
def riscv_ecall(
    imm: UDynamic,
    rs1: Wide,
    rd: Wide,
    x0: Wide,
    x1: Wide,
    x2: Wide,
    x3: Wide,
    x4: Wide,
    x5: Wide,
    x6: Wide,
    x7: Wide,
    x8: Wide,
    x9: Wide,
    x10: Wide,
    x11: Wide,
    x12: Wide,
    x13: Wide,
    x14: Wide,
    x15: Wide,
    x16: Wide,
    x17: Wide,
    x18: Wide,
    x19: Wide,
    x20: Wide,
    x21: Wide,
    x22: Wide,
    x23: Wide,
    x24: Wide,
    x25: Wide,
    x26: Wide,
    x27: Wide,
    x28: Wide,
    x29: Wide,
    x30: Wide,
    x31: Wide,
    memory: Array,
    pc: Wide,
    exit: Unit,
) -> ToConvert:
    x17_buff = Wide("x17_buff", (x17[0],))

    def _ecall_close() -> ToConvert:
        return store_array(memory, UDynamic.from_int(0, 4), x10)

    def _ecall_lseek() -> ToConvert:
        return store_array(memory, UDynamic.from_int((1 << 32) - 29), x10)

    def _ecall_exit() -> ToConvert:
        return clear_unit(exit)

    def _ecall_print() -> ToConvert:
        addr = Wide.from_length("addr", 4)
        counter = Wide.from_length("counter", 4)
        yield add_wide(x11, UDynamic.from_int(0, 4), addr)
        yield add_wide(x12, UDynamic.from_int(0, 4), counter)

        char = Unit("char")
        yield loop_wide(
            counter,
            macrocode(
                load_array(memory, Wide("char", (char,)), addr),
                output(char),
                clear_unit(char),
                add_wide(addr, UDynamic.from_int(1, 4), addr),
                sub_wide(counter, UDynamic.from_int(1, 4), counter),
            ),
        )

        yield clear_wide(addr), clear_wide(counter)
        return free_wide(addr), free_wide(counter)

    close_result = _ecall_close()
    lseek_result = _ecall_lseek()
    exit_result = _ecall_exit()
    print_result = _ecall_print()

    cases: dict[UDynamic, CoreOpcode] = {
        UDynamic.from_int(62, 1): macrocode(lseek_result),
        UDynamic.from_int(64, 1): macrocode(print_result),
        UDynamic.from_int(57, 1): macrocode(close_result),
        UDynamic.from_int(93, 1): macrocode(exit_result),
        UDynamic.from_int(10, 1): NOP,
    }

    yield switch_wide(x17_buff, cases, NOP)
    yield clear_wide(x17_buff), free_wide(x17_buff)
    return None
