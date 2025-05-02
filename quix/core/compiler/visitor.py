from typing import override

from quix.core.compiler.base import CoreVisitor
from quix.core.interfaces.writable import Writable
from quix.core.opcodes.dtypes import Code, CoreProgram, Ref, Value
from quix.core.values import BFCommands

from .pointer import BFPointer


class BFVisitor(CoreVisitor):
    __slots__ = (
        "_dest",
        "_ptr",
    )

    def __init__(
        self,
        dest: Writable,
        pointer: BFPointer | None = None,
    ) -> None:
        self._dest = dest
        self._ptr = pointer or BFPointer.default()

    @override
    def add(self, ref: Ref | None, value: Value) -> None:
        self._move_pointer(ref)
        command = BFCommands.DEC if value < 0 else BFCommands.INC
        self._dest.write(command * abs(value))

    @override
    def input(self, ref: Ref | None) -> None:
        self._move_pointer(ref)
        self._dest.write(BFCommands.STDIN)

    @override
    def output(self, ref: Ref | None) -> None:
        self._move_pointer(ref)
        self._dest.write(BFCommands.STDOUT)

    @override
    def loop(self, ref: Ref | None, program: CoreProgram) -> None:
        self._move_pointer(ref)
        self._dest.write(BFCommands.START_LOOP)
        self.visit(program)
        self._move_pointer(ref)
        self._dest.write(BFCommands.END_LOOP)

    @override
    def inject(self, ref: Ref | None, code: Code, exit: Ref | None, sortable: bool = False) -> None:
        self._move_pointer(ref)
        self._dest.write(code)
        self._move_pointer(exit, gen_code=False)

    def _move_pointer(self, ref: Ref | None, *, gen_code: bool = True) -> None:
        code = self._ptr.move_by_ref(ref)
        if gen_code:
            self._dest.write(code)
