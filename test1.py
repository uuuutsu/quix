from quix.bootstrap.dtypes import Str
from quix.core.opcodes import add

value = Str.from_value("Hello, World!")

program = add(value, 1)
