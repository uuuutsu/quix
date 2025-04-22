from typing import override

from quix.core.interfaces.writable import Writable
from quix.core.opcodes import CoreOpcode
from quix.core.opcodes.dtypes import Code, Program, Ptr, Value
from quix.core.visitor.base import CoreVisitor

from .commands import BFCommands
from .pointer import BFPointer


class BFVisitor(CoreVisitor):
    __slots__ = (
        "_dest",
        "_ptr",
    )

    def __init__(self, dest: Writable, pointer: BFPointer | None = None) -> None:
        self._dest = dest
        self._ptr = pointer or BFPointer.default()

    @override
    def add(self, ptr: Ptr, value: Value) -> None:
        self._move_pointer(ptr)
        command = BFCommands.DEC if value < 0 else BFCommands.INC
        self._dest.write(command * abs(value))

    @override
    def input(self, ptr: Ptr) -> None:
        self._move_pointer(ptr)
        self._dest.write(BFCommands.STDIN)

    @override
    def output(self, ptr: Ptr) -> None:
        self._move_pointer(ptr)
        self._dest.write(BFCommands.STDOUT)

    @override
    def loop(self, ptr: Ptr, program: Program[CoreOpcode]) -> None:
        self._move_pointer(ptr)
        self._dest.write(BFCommands.START_LOOP)
        self.visit(program)
        self._move_pointer(ptr)
        self._dest.write(BFCommands.END_LOOP)

    @override
    def inject(self, ptr: Ptr, code: Code, exit: Ptr) -> None:
        self._move_pointer(ptr)
        self._dest.write(code)
        self._move_pointer(exit, gen_code=False)

    def _move_pointer(self, ptr: Ptr, *, gen_code: bool = True) -> None:
        code = self._ptr.move(ptr)
        if gen_code:
            self._dest.write(code)
