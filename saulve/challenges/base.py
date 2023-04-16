from typing import NamedTuple, Protocol

from ..errors import PuzzleNotFound, ValidationError
from ..puzzle import Puzzle


class PuzzleView(NamedTuple):
    """A representation of a puzzle for display purpose."""
    id: str
    name: str


class Challenge(Protocol):
    """A collection of puzzle from a common source.
    """
    def find(self) -> list[PuzzleView]:
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
