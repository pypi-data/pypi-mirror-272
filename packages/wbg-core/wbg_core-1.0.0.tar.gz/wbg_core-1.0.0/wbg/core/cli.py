"""Utilities for CLI scripts."""
import argparse
from . import env


def configure_parser(
    parser: argparse.ArgumentParser,
    flag: str = '--prd',
    dest: str = 'env',
) -> None:
    """Set arguments on parser."""
    parser.add_argument(
        flag,
        action='store_const',
        const=env.Env.PRD,
        default=env.Env.TST,
        help='Runtime type',
        dest=dest,
    )
