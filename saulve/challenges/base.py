from typing import Protocol

from ..errors import PuzzleNotFound, ValidationError
from ..puzzle import Puzzle


class Challenge(Protocol):
    """A collection of puzzle from a common source.
    """
    def find(self) -> list[Puzzle]:
        """Get all known puzzles"""

    def get(self, *args: str) -> Puzzle:
        """Get a single puzzle.

        Arguments:
            *args (str): Id of the puzzle. Can be any list of strings, details
                depends on the actual implementation.

        Raises:
            PuzzleNotFound: If no puzzle exists for the given id
            ValidationError: If the argument aren't valid for puzzle selection
        """


class ChallengeLoader(Protocol):
    def load(self) -> Challenge:
        ...
