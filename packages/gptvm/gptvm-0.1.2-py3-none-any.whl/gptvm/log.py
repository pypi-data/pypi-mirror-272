import logging
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="%X", handlers=[RichHandler()]
)

logger = logging.getLogger(__package__)
logger.setLevel(logging.INFO)

def logger_set_debug():
    logger.setLevel(logging.DEBUG)