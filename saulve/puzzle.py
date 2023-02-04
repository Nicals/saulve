"""Declare puzzle and their associated solution.
"""

from typing import Callable, Generic, NamedTuple, TypeVar

from .errors import PuzzleHasNoSolution


__all__ = ['Puzzle']


class PuzzleSolution(NamedTuple):
    """
    The result of one stage of a puzzle.
    """
    solution: str | None

    @property
    def is_solved(self) -> bool:
        return self.solution is not None


PuzzleInput = TypeVar('PuzzleInput')

PuzzleStepResult = int | str | None

SolutionFunction = Callable[[PuzzleInput], PuzzleStepResult]


class Puzzle(Generic[PuzzleInput]):
    """Holds solutions of a puzzle and its input data.

    A puzzle is first defined by its name and input.
    Next, some solution functions steps are registered by decorating them with
    the `solution` decorator.

    Arguments:
        name: A verbose name for this puzzle
        puzzle_input: The input data of the puzzle.

    Attributes:
        name: A verbose title for the current puzzle
        puzzle_input: Input problem to solve
        steps: A list of callable implementing puzzle solutions
    """
    def __init__(self, name: str, puzzle_input: PuzzleInput|None = None) -> None:
        self.name = name
        self.puzzle_input = puzzle_input
        self.steps: list[SolutionFunction] = []

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: {self.name}>'

    def __str__(self) -> str:
        return self.name

    def solution(
        self,
        fn: SolutionFunction,
    ) -> SolutionFunction:
        """Register a solution function for the puzzle.

        The function takes the puzzle input as argument and should return a
        solution.

        Example:
            >>> puzzle = Puzzle(title="double", puzzle_input=12)
            >>> @puzzle.solution
            ... def double_input(number):
            ...     return number * 2
        """
        self.steps.append(fn)
        return fn

    def solve(self) -> list[PuzzleSolution]:
        """Run all registered solutions for this puzzle and return a list of
        solution values.

        Raises:
            PuzzleHasNoSolution: If no solution have been registered for this
                puzzle.
        """
        if not self.steps:
            raise PuzzleHasNoSolution(
                f"{self} don't have registered solutions"
            )

        solutions: list[PuzzleSolution] = []

        for solve_step in self.steps:
            solution = solve_step(self.puzzle_input)

            solutions.append(PuzzleSolution(
                str(solution) if solution is not None
                else None
            ))

        return solutions
