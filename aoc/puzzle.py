"""Holds puzzle solving.
"""

from pathlib import Path
from typing import Any, Callable, Generic, IO, NamedTuple, TypeVar

from .errors import PuzzleInputMissing


__all__ = ['Puzzle', 'Solution']


T = TypeVar('T')


class Solution(Generic[T]):
    """This class should be implemented when solving challenges.

    Type:
        T: Type of the puzzle input once parsed by `parse_input_file`.
    """
    def parse_input_file(self, file: IO[str]) -> T:
        """
        Parsed puzzle input file.

        Returns:
            T: Input data that will be passed as argument to `first_star` and
                `second_star`.
        """

    def first_star(self, puzzle: T) -> int | str | None:
        """
        Implement this to solve the first stage of this challenge.

        Arguments:
            puzzle (T): Puzzle input as returned by `parse_input_file`.

        Returns:
            int | str: Actual solution to the puzzle.
            None: if the puzzle is not solved.
        """

    def second_star(self, puzzle: T) -> int | str | None:
        """
        Implement this to solve the first stage of this challenge.

        See:
            first_star: for arguments and return value meaning.
        """


# Types one of the Solution.{first_star,second_star} method;
# I'm not really sure how to type this... The Any should be the T type # of
# the Solution class
SolutionMethod = Callable[[Any], int | str | None]


class StarResult(NamedTuple):
    """
    The result of one stage of a puzzle.
    """
    solution: str | None

    @property
    def is_solved(self):
        return self.solution is not None


class PuzzleResult(NamedTuple):
    """
    The whole result of a puzzle
    """
    first_star: StarResult
    second_star: StarResult

    @property
    def is_solved(self):
        return self.first_star.is_solved and self.second_star.is_solved


class Puzzle:
    def __init__(
        self,
        year: int,
        day: int,
        solution: Solution,
        input_path: Path | None,
    ) -> None:
        self.year, self.day = year, day
        self.solution = solution
        self.input_path = input_path

    def _run_star(
        self,
        star_func: SolutionMethod,
        puzzle_input: str,
    ) -> StarResult:
        result = star_func(puzzle_input)

        return StarResult(solution=str(result) if result is not None else None)

    def run(self) -> PuzzleResult:
        """
        Raise:
            PuzzleInputMissing: If no input are provided to run the puzzle
                against.
        """
        if self.input_path is None:
            raise PuzzleInputMissing()

        with self.input_path.open() as f:
            puzzle_input = self.solution.parse_input_file(f)

        first_star = self._run_star(self.solution.first_star, puzzle_input)
        second_star = self._run_star(self.solution.second_star, puzzle_input)

        return PuzzleResult(first_star, second_star)
