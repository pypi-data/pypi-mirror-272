import os
import click
from dotenv import load_dotenv
from .commands import InstallCommand
from .logger import ClickLogger


@click.group()
def cli():
    load_dotenv()


@cli.command("install")
def install():
    debug = os.environ.get("DEBUG", None)
    logger = ClickLogger(level=1 if debug else 2)
    InstallCommand(logger=logger).run()
