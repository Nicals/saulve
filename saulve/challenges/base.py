from typing import Protocol

from ..puzzle import Puzzle


class Challenge(Protocol):
    """A collection of puzzle from a common source.
    """
    def get(self, *args: str) -> Puzzle:
        ...


class ChallengeLoader(Protocol):
    def load(self) -> Challenge:
        ...
