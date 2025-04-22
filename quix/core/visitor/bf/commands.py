from enum import StrEnum


class BFCommands(StrEnum):
    INC: str = "+"
    DEC: str = "-"

    MOVE_LEFT: str = "<"
    MOVE_RIGHT: str = ">"

    START_LOOP: str = "["
    END_LOOP: str = "]"

    STDIN: str = ","
    STDOUT: str = "."
