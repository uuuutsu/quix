import json
from typing import Any

from typer import Exit, colors, secho


def _error_exit(message: str, exception: Exception, code: int = 1) -> None:
    secho(f"Error: {message}", err=True, fg=colors.RED)
    secho(f"Details: {exception}", err=True, fg=colors.BRIGHT_BLACK)
    raise Exit(code=code) from exception


def save_json(file_name: str, data: dict[str, Any]) -> None:
    try:
        with open(f"{file_name}.json", "w") as json_file:
            json.dump(data, json_file, indent=4)
    except Exception as e:
        _error_exit(f"Failed to save JSON to {file_name}.json", e)


def save_file(file: str, data: Any) -> None:
    try:
        with open(file, "w") as f:
            f.write(data)
    except Exception as e:
        _error_exit(f"Failed to write to file {file}", e)


def read_file(file: str) -> str | None:
    try:
        with open(file) as f:
            return f.read()
    except FileNotFoundError as e:
        _error_exit(f"File {file} not found", e)
        return None
    except UnicodeError as e:
        _error_exit("Unicode error occurred while reading the file", e)
        return None
    except Exception as e:
        _error_exit(f"Failed to read file {file}", e)
        return None
