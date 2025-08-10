import time
from typing import Optional

import typer
from typer import Exit, Option, secho

from quix.cli.utils import datatool
from quix.exec.simple import Executor, Memory

app = typer.Typer()


def execute_code(executor: Executor, output: Optional[str] = None, stats: Optional[str] = None) -> str:
    start = time.time()

    executor_output = executor.run().output
    if not executor_output:
        secho("No code output. Terminating")
        raise Exit(code=1)

    code_output = executor_output.getvalue()

    if output:
        datatool.save_file(output, code_output)
    if stats:
        exc_time = time.time() - start
        memory_state = executor.memory.cells
        stats_json = {"execution_time": exc_time, "memory": memory_state}

        datatool.save_json(file_name=stats, data=stats_json)

    return code_output


@app.command("exec")
def run_exec(
    file: str = Option(None, "--file", "-f", help="Path to source file"),
    code: str = Option(None, "--code", "-c", help="Inline code"),
    memory: int = Option(256, "--memory", "-m", help="Maximum memory cells"),
    executor: str = Option("simple", "--executor", "-e", help="Executor used to compile the code"),
    output: str = Option(None, "--output", "-o", help="Write the output of the program to a file"),
    stats: str = Option(None, "--stats", "-s", help="Store execution stats in a file"),
) -> None:
    if file and code:
        secho("Choose either file(-f) or code(-c), not both.")
        raise Exit(code=1)
    if not file and not code:
        secho("You must choose to either run code from file(-f) or code(-c).")
        raise Exit(code=1)
    executable_code = datatool.read_file(file) if file else code

    if not executable_code:
        secho("No code provided. Terminating.")
        raise Exit(code=1)

    if executor:
        match executor.lower():
            case "simple":
                memory_size = Memory(size=memory)
                code_executor = Executor(executable_code, memory=memory_size)
            case _:
                secho("Use --help to see available executor options.")

    code_output = execute_code(executor=code_executor, output=output, stats=stats)

    secho(code_output)
