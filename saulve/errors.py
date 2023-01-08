"""
Saulve related errors.
"""

from typing import Type


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


class ModuleImportError(SaulveError):
    """Raised when we fail to dynamically load modules."""


class MissingAttribute(ModuleImportError):
    """Raised when an expected attribute is missing from an imported module."""
    def __init__(self, module_name: str, attr: str) -> None:
        msg = f"{module_name} does not have a '{attr}' attribute."
        super().__init__(msg)


class WrongAttributeType(ModuleImportError):
    """Raised when an imported module attribute is not of the expected type."""
    def __init__(self, attr_name: str, expected_type: Type) -> None:
        msg = f"{attr_name} is not a {expected_type.__name__} instance."
        super().__init__(msg)
