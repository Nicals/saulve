"""
AOC related errors.
"""


class AOCError(Exception):
    """Base class for aoc related errors."""


class ValidationError(Exception):
    """Raised when user input is not valid."""


class PuzzleHasNoSolution(Exception):
    """Raised when a puzzle don't have any registered solution."""


class ChallengeNotFound(AOCError):
    """Raised when a challenge does not exist."""


class PuzzleNotFound(AOCError):
    """Raised when a puzzle does not exist."""


class PuzzleModuleError(AOCError):
    """Raised when we fail to load a puzzle module."""
