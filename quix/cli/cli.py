import typer

from quix.cli.commands import execute

app = typer.Typer(name="quix")


app.add_typer(execute.app)


if __name__ == "__main__":
    app()
