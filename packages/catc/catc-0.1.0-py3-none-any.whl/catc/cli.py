import os
from os.path import join
import click
from .concatenator import Concatenator
from .config import Config, CONFIG_FILE_NAME
from .logger import ClickLogger


@click.command()
@click.argument("path", type=click.Path(exists=True))
def catc(path: str):
    debug = os.getenv("DEBUG", None)
    logger = ClickLogger(level=1 if debug else 0)

    config = Config.from_file(join(path, CONFIG_FILE_NAME))
    Concatenator(logger=logger).concat(path, config)
