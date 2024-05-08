"""
Shell utilities.
"""

from __future__ import annotations

import time
import datetime


def sleep(interval_mins: float, sleep_block_seconds: int = 60) -> None:
    """Pause execution with shell sleep, to avoid hibernation of process.

    Required for programs running in externally created pwsh process
    >>> sleep(10)
    """
    seconds = int(interval_mins * 60)
    block = seconds // sleep_block_seconds
    print(
        f'Started sleep at {_timestamp(datetime.datetime.now())}, sleep block seconds = {sleep_block_seconds}'
    )

    for iteration in range(block):
        print(f'\rSleeping for {block - iteration} more blocks--{iteration = }', end='')
        time.sleep(sleep_block_seconds)

    print(f'\nCompleted at {_timestamp(datetime.datetime.now())}')


def _timestamp(timestamp: datetime.datetime) -> str:
    return f'{timestamp:%F %X}'
