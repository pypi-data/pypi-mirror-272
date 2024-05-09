import logging
import logging.handlers
from typing import List
import sys

FORMAT = "[%(asctime)s | %(module)s | %(levelname)s | %(lineno)d]: %(message)s"
DATETIME_FMT = "%Y-%m-%dT%H:%M:%S%z"


def logging_config(
    logger_level: str | int = logging.INFO,
    logger_fmt: str = FORMAT,
    logger_dt_fmt: str = DATETIME_FMT,
) -> None:
    """Default configuration logger.

    ..code::
        # main.py o any
        import logging
        ...
        import setup_logger # or the name of the this module
        ...
        setup_logger.logging_config()  # or the name of this function
        logger = logging.getLogger(__name__)
        ...

        # For any other module use the standar
        import logging
        ...
        logger = logging.getLogger(__name__)

    For other logger is possible to configure separete as
    setLevel or Propagate:

    .. code::
        logging.getLogger("pkg_name").setLevel("LEVEL")
        logging.getLogger("pkg_name").propagate = False
    """
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    logging.basicConfig(
        level=logger_level,
        format=logger_fmt,
        datefmt=logger_dt_fmt,
        handlers=(stream_handler,),
    )


def disable_logger(loggers: List[str]) -> None:
    """Disable some loggers.

    logging.getLogger("urllib3").setLevel(logging.WARNING)
    """
    for logger in loggers:
        logging.getLogger(logger).setLevel(logging.WARNING)


def _show_loggers() -> None:
    """Print all loggers for entire application.

    Require import all modules to show all loggers available.

    ..code::

        import A
        import B
        ...

    Ref: https://stackoverflow.com/a/36208664/4112006
    """
    # import celery  # noqa: F401
    # import requests  # noqa: F401
    print("Available loggers:")
    for logger in logging.Logger.manager.loggerDict:
        print(logger)


def get_logger(logger_name, level: int = logging.INFO) -> logging.Logger:
    logging_config(level)
    return logging.getLogger(logger_name)


if __name__ == "__main__":
    _show_loggers()
