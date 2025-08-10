import io
from dataclasses import dataclass, field
from typing import Self

from bidict import bidict

from .memory import Memory
from .utils import build_jump_map


@dataclass
class Executor:
    code: io.StringIO | str
    input: io.StringIO | None = None
    output: io.StringIO | None = None
    memory: Memory = field(default_factory=Memory)
    pc: int = field(init=False, default=0)
    jump_map: bidict[int, int] = field(init=False, default_factory=bidict)

    def run(self) -> Self:
        if isinstance(self.code, io.StringIO):
            self.code = self.code.getvalue()

        if self.output is None:
            self.output = io.StringIO()

        self.jump_map = build_jump_map(self.code)
        while self.pc < len(self.code):
            self._execute_command(self.code[self.pc])
            self.pc += 1

        return self

    def _execute_command(self, command: str) -> None:
        match command:
            case ">":
                self.memory.increment_ptr()
            case "<":
                self.memory.decrement_ptr()
            case "-":
                self.memory.decrement_data()
            case "+":
                self.memory.increment_data()
            case "[":
                if not self.memory.load():
                    self.pc = self.jump_map[self.pc]
            case "]":
                if self.memory.load():
                    self.pc = self.jump_map.inverse[self.pc]
            case ",":
                if self.input:
                    self.memory.store(self.input.read(1))
                    return

                self.memory.store(input()[0])
            case ".":
                if self.output:
                    self.output.write(chr(self.memory.load()))
                    return
