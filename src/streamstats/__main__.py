import typer
from typing import Annotated

from streamstats.report import make_report

app = typer.Typer()

@app.command()
def analyze(
        INPUT: Annotated[str, typer.Argument()],
        FORMAT: Annotated[str, typer.Option("--format")],
        OUTPUT: Annotated[str, typer.Option("--output")] = "report.json",
        SKIP_INVALID: Annotated[bool, typer.Option("--skip-invalid")] = False
):
    make_report(INPUT, FORMAT, OUTPUT, skip_invalid=SKIP_INVALID)

@app.command()
def void():
    pass


if __name__ == "__main__":
    app()