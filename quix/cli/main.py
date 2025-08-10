import typer

from quix.cli.commands import build, execute

app = typer.Typer(name="quix")


app.add_typer(execute.app)
app.add_typer(build.app)


if __name__ == "__main__":
    app()
