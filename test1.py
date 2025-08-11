from quix.bootstrap.dtypes import Str
from quix.core.opcodes import add

value = Str.from_value("Hello, World!")

add(value, 1)
