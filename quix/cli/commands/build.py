import importlib
from typing import Final

import typer
from typer import Exit, Option, secho

from quix.cli.compiler import bf_compiler
from quix.cli.utils import datatool
from quix.cli.utils.error_handler import _error_exit
from quix.core.opcodes.base import CoreOpcode

app = typer.Typer()

MAX_PRINT_SIZE: Final[int] = 128


def get_var(module: str) -> list[CoreOpcode] | None:
    """
    Gets value of a variable from specified python module.
    """
    try:
        module_name, var_name = module.split(":")
    except ValueError as e:
        _error_exit(message="Incorrect path format. Use --help for more information", exception=e)
        return None
    try:
        imported_module = importlib.import_module(module_name)
        if module:
            var: list[CoreOpcode] = getattr(imported_module, var_name)
        return var
    except Exception as e:
        _error_exit(message=f"Failed to get {module}", exception=e)
        return None


@app.command("ass")
def ass(
    path: str = Option(None, "--path", "-p", help="Path to variable in format module.submodule:variable"),
    output: str = Option(None, "--output", "-o", help="Write the output of the program to a file"),
    memory_layout: str = Option(None, "--layout", "-l", help="Write memory layout of the program to a file"),
    garbage_collector: bool = Option(False, "--garbage", "-g", help="Enable garbage collector"),
) -> None:
    if not path:
        secho("Specify path to variable in format module.submodule:variable")
        raise Exit(code=1)

    opcodes: list[CoreOpcode] | None = get_var(path)

    if not opcodes:
        _error_exit(message="Specified path does not contain opcodes", exception=ValueError(f"{path} does not exist"))
        raise Exit(code=1)

    result = bf_compiler.compile_seq(opcodes, garbage_collector)

    if not result:
        secho("Unable to compile opcodes")
        raise Exit(code=1)

    bf_code, layout = result

    if len(bf_code) <= MAX_PRINT_SIZE:
        secho(bf_code)
    else:
        secho("Output length is too big. Saving output in 'output.bf'")
        output = "output"

    formatted_layout = {str(key): value for key, value in layout.items()}
    if memory_layout:
        datatool.save_json(memory_layout, formatted_layout)

    if output:
        datatool.save_file(file_name=output, extension="bf", data=bf_code)


@app.command("build")
def redirect(
    path: str = Option(None, "--path", "-p", help="Path to variable in format module.submodule:variable"),
    output: str = Option(None, "--output", "-o", help="Write the output of the program to a file"),
    memory_layout: str = Option(None, "--layout", "-l", help="Write memory layout of the program to a file"),
    garbage_collector: bool = Option(False, "--garbage", "-g", help="Enable garbage collector"),
) -> None:
    """
    Used as 'safe' alternative for ass command
    """
    ass(path, output, memory_layout, garbage_collector)
