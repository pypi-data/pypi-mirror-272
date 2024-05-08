import json
import logging

import rich.progress
import typer
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

FORMAT = "%(message)s"
logging.basicConfig(
    level="ERROR", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")

console = Console()
app = typer.Typer()


@app.command()
def setup():
    """
    Generate a configuration file template using pineapple.
    """
    project = Prompt.ask("Project name")
    console.print("[dim]View documentation to see what 'version' tag does.")
    version = Prompt.ask("Version")

    # Generate a temporary configuration file.
    temp = {
        "metadata": {
            "project": f"{project}",
            "version": f"{version}",
        },

        "settings": {
            "pineapple-api": "1",
            # Other settings goes here...
        },

        "files": {
            # Your files to be included will reside here.
        }
    }

    console.print(Panel.fit(f"[green]Project name: {project}\nVersion: {version}", title="JSON Configuration"))

    temp_good = Confirm.ask("Continue with generation?", default=True)
    if temp_good:

        with console.status("[bold green]Generating configuration file...") as status:
            with open('pineapple.json', 'w') as config:
                json.dump(temp, config, indent=3)

        console.print(
            '[yellow]Pineapple[/yellow] configuration is [green]done generating![/green] [blue]Visit the '
            'documentation to view options.')
    else:
        console.print("[red]Generation of configuration file aborted.")


@app.command()
def clone(url: str):
    """
    Grabs a GitHub URL and clones the repository, deletes all unnecessary files and only leaves specified files for the user.
    """


@app.command()
def verify(debug: bool = False):
    """
    Useful for ensuring that local pineapple configuration file remains OK and functional.
    """
    # Set outer variables
    config = None
    metadata = None
    settings = None
    files = None

    if debug:
        log.setLevel("DEBUG")
        log.debug("Starting configuration verification...")
        log.debug("Using [green]v1 API[/green] for verification...", extra={"markup": True})

        try:
            with rich.progress.open("pineapple.json", "rb", description="Loading config...") as file:
                config = json.load(file)
            metadata = config["metadata"]
            log.debug("[dim]Loaded metadata... :white_check_mark:", extra={"markup": True})
            settings = config["settings"]
            log.debug("[dim]Loaded settings... :white_check_mark:", extra={"markup": True})
            files = config["files"]
            log.debug("[dim]Loaded files... :white_check_mark:", extra={"markup": True})
        except FileNotFoundError:
            log.exception("'pineapple.json' was not found in root folder of project.")
            exit()

        log.info("[blue]Configuration file was loaded. Proceeding with next step...", extra={"markup": True})
        log.debug("Starting verification, verify API is valid version.")

        if settings["pineapple-api"] == '1':
            log.debug("Configuration file is using [green]v1 API.[/green] Continuing with verification...",
                      extra={"markup": True})
        else:
            log.critical("Configuration file has invalid API version number.")
            exit(1)

    else:
        console.log("Verbose off")


if __name__ == "__main__":
    app()
