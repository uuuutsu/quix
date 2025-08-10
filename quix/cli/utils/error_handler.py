from typer import Exit, colors, secho


def _error_exit(message: str, exception: Exception, code: int = 1) -> None:
    secho(f"Error: {message}", err=True, fg=colors.RED)
    secho(f"Details: {exception}", err=True, fg=colors.BRIGHT_BLACK)
    raise Exit(code=code) from exception
