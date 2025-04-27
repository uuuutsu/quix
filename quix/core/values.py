from enum import StrEnum


class BFCommands(StrEnum):
    INC = "+"
    DEC = "-"

    MOVE_LEFT = "<"
    MOVE_RIGHT = ">"

    START_LOOP = "["
    END_LOOP = "]"

    STDIN = ","
    STDOUT = "."
