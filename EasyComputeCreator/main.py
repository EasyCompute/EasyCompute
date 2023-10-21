import logging
from pathlib import Path

import click

from src.compute_creator import ComputeCreator
from src.utils.log import setup_logging

logger = logging.getLogger(__name__)


@click.command()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
def main(verbose):
    setup_logging(verbose=verbose)

    logger.info("Building Compute Instance")
    ComputeCreator().build_compute_instance()


if __name__ == "__main__":
    main()
