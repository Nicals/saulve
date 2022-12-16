"""
AOC related errors.
"""


class AOCError(Exception):
    """Base class for aoc related errors."""


class PuzzleNotFound(AOCError):
    """Raised when a puzzle does not exist."""


class PuzzleInputMissing(AOCError):
    """Raised when a puzzle input is missing."""


class SolutionModuleError(AOCError):
    """Raised when we fail to load a puzzle module."""
