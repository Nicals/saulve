"""
Saulve related errors.
"""


class SaulveError(Exception):
    """Base class for saulve related errors."""


class ValidationError(Exception):
    """Raised when user input is not valid."""


class PuzzleHasNoSolution(Exception):
    """Raised when a puzzle don't have any registered solution."""


class ChallengeNotFound(SaulveError):
    """Raised when a challenge does not exist."""


class PuzzleNotFound(SaulveError):
    """Raised when a puzzle does not exist."""


class PuzzleModuleError(SaulveError):
    """Raised when we fail to load a puzzle module."""
