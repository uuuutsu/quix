from quix.core.interfaces import Readable
from quix.core.opcodes import CoreOpcode, CoreProgram, Ref, add, input, output
from quix.core.opcodes.opcodes import end_loop, start_loop
from quix.core.values import BFCommands
from quix.tools import generate_unique_id


def decompile(
    source: Readable,
    start_ptr: int = 0,
    start_memory: dict[int, Ref] | None = None,
) -> tuple[CoreProgram, dict[int, Ref]]:
    loop_stack: list[int] = []
    program: list[CoreOpcode] = []
    curr_ptr: int = start_ptr
    memory = start_memory or {}

    def get_current_ref() -> Ref:
        if curr_ptr not in memory:
            memory[curr_ptr] = generate_unique_id()
        return memory[curr_ptr]

    while command := source.read(1):
        match command:
            case BFCommands.INC:
                program.append(add(get_current_ref(), 1))
            case BFCommands.DEC:
                program.append(add(get_current_ref(), -1))
            case BFCommands.MOVE_LEFT:
                curr_ptr -= 1
            case BFCommands.MOVE_RIGHT:
                curr_ptr += 1
            case BFCommands.STDIN:
                program.append(input(get_current_ref()))
            case BFCommands.STDIN:
                program.append(output(get_current_ref()))
            case BFCommands.START_LOOP:
                loop_stack.append(curr_ptr)
                program.append(start_loop(get_current_ref()))
            case BFCommands.END_LOOP:
                if not loop_stack:
                    raise RuntimeError("Unopened loop")
                old_ptr = loop_stack.pop()
                if curr_ptr != old_ptr:
                    raise RuntimeError("Unbalanced loops are not supported")

                program.append(end_loop())

    if loop_stack:
        raise ValueError("Unclosed loop.")

    return program, memory
