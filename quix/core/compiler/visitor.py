from typing import override

from quix.core.compiler.base import CoreVisitor
from quix.core.compiler.types import Ptr
from quix.core.interfaces.writable import Writable
from quix.core.opcodes.dtypes import Code, Ref, Value
from quix.core.values import BFCommands

from .pointer import BFPointer


class BFVisitor(CoreVisitor):
    __slots__ = (
        "_dest",
        "_ptr",
        "_stack",
    )

    def __init__(
        self,
        dest: Writable,
        pointer: BFPointer | None = None,
    ) -> None:
        self._dest = dest
        self._ptr = pointer or BFPointer.default()
        self._stack: list[Ptr] = []

    @override
    def add(self, ref: Ref | None, value: Value) -> None:
        self._move_pointer_by_ref(ref)
        command = BFCommands.DEC if value < 0 else BFCommands.INC
        self._dest.write(command * abs(value))

    @override
    def input(self, ref: Ref | None) -> None:
        self._move_pointer_by_ref(ref)
        self._dest.write(BFCommands.STDIN)

    @override
    def output(self, ref: Ref | None) -> None:
        self._move_pointer_by_ref(ref)
        self._dest.write(BFCommands.STDOUT)

    @override
    def start_loop(self, ref: Ref | None) -> None:
        self._stack.append(self._ptr.get_ptr(ref))
        self._move_pointer_by_ref(ref)
        self._dest.write(BFCommands.START_LOOP)

    @override
    def end_loop(self) -> None:
        if not self._stack:
            raise RuntimeError("Unopened loop")
        self._move_pointer_by_ptr(self._stack.pop())
        self._dest.write(BFCommands.END_LOOP)

    @override
    def inject(self, ref: Ref | None, code: Code, exit: Ref | None, sortable: bool = False) -> None:
        self._move_pointer_by_ref(ref)
        self._dest.write(code)
        self._move_pointer_by_ref(exit, gen_code=False)

    def _move_pointer_by_ref(self, ref: Ref | None, *, gen_code: bool = True) -> None:
        code = self._ptr.move_by_ref(ref)
        if gen_code:
            self._dest.write(code)

    def _move_pointer_by_ptr(self, ptr: Ptr, *, gen_code: bool = True) -> None:
        code = self._ptr.move_by_ptr(ptr)
        if gen_code:
            self._dest.write(code)
