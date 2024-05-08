"""Logging utilities."""

import logging
import pathlib


FORMAT = "%(asctime)s:%(levelname)s:%(module)s:%(funcName)s %(message)s"
DATE_FMT = "%FT%T"


def setup_root_logger(
    logfile: pathlib.Path, level: int = logging.DEBUG, force_override: bool = False
) -> None:
    """Common setup for logging."""
    _log_formatter = logging.Formatter(FORMAT, DATE_FMT)

    fh = logging.FileHandler(logfile)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(_log_formatter)
    logging.basicConfig(
        format=FORMAT,
        datefmt=DATE_FMT,
        level=level,
        force=force_override,
        handlers=[logging.StreamHandler(), fh],
    )
