import re
import typing

pattern: typing.Final[re.Pattern[str]] = re.compile(r"(?<!^)(?=[A-Z])")


def camel_case_to_snake_case(string: str, /) -> str:
    return pattern.sub("_", string).lower()


def snake_case_to_camel_case(string: str, /) -> str:
    first, *others = string.split("_")
    return ''.join([first.lower(), *map(str.title, others)])

