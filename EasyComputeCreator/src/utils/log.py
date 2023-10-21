import logging

import coloredlogs
from __version__ import version

logger = logging.getLogger(__name__)


def setup_logging(verbose: bool = False) -> None:
    coloredlogs.install(
        level=logging.DEBUG if verbose else logging.INFO,
        fmt=f"[%(asctime)s.%(msecs)03d] [%(levelname).3s] %(message)s",
        datefmt="%M%S",
    )

    # ASCII Art Generator : https://patorjk.com/software/taag/
    banner = r"""
   _____                          ___              
  / ___/__  ______  ___  _____   /   |  ____  ____ 
  \__ \/ / / / __ \/ _ \/ ___/  / /| | / __ \/ __ \
 ___/ / /_/ / /_/ /  __/ /     / ___ |/ /_/ / /_/ /
/____/\__,_/ .___/\___/_/     /_/  |_/ .___/ .___/ 
          /_/                       /_/   /_/      
"""

    logger.info(banner)
    logger.info(f"Version: {version}")
