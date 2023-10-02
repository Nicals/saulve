"""Loads challenge from memory.

This module should be useful for testing purpose.
"""

from saulve.puzzle import Puzzle

from .base import Challenge, ChallengeLoader
from .generic import Challenge as GenericChallenge


class InMemoryLoader(ChallengeLoader):
    def __init__(self, puzzles: list[Puzzle]) -> None:
        self.puzzles = puzzles

    def load(self) -> Challenge:
        return GenericChallenge({
            str(i): puzzle
            for (i, puzzle) in enumerate(self.puzzles)
        })
