"""Environment configuration."""
from __future__ import annotations
import enum


class Env(enum.StrEnum):
    """Runtime environment flag."""

    PRD = enum.auto()
    TST = enum.auto()

    @classmethod
    def from_bool(cls, is_prd: bool) -> Env:
        """Return env from bool flag."""
        return Env.PRD if is_prd else Env.TST
