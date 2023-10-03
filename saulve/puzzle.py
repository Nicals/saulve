"""Declare puzzle and their associated solution.
"""

from typing import Callable, Concatenate, NamedTuple, ParamSpec, TypeVar

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


PuzzleStepResult = int | str | None

T = TypeVar('T')
U = TypeVar('U')

P = ParamSpec('P')


class Puzzle:
    """Holds solutions of a puzzle and its input data.

    A puzzle is first defined by its name and input.
    Next, some solution functions steps are registered by decorating them with
    the `solution` decorator.

    Arguments:
        name: A verbose name for this puzzle

    Attributes:
        name: A verbose title for the current puzzle
        steps: A list of callable implementing puzzle solutions
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.steps: list[Callable[[], PuzzleStepResult]] = []

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: {self.name}>'

    def __str__(self) -> str:
        return self.name

    def with_input(self, puzzle_input: U) -> Callable[
        [Callable[Concatenate[U, P], T]],
        Callable[P, T],
    ]:
        def decorator(fn: Callable[Concatenate[U, P], T]) -> Callable[P, T]:
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                return fn(puzzle_input, *args, **kwargs)

            return wrapper

        return decorator  # type: ignore[return-value] # pending issue 9

    def solution(
        self,
        fn: Callable[[], PuzzleStepResult],
    ) -> Callable[[], PuzzleStepResult]:
        """Register a solution function for the puzzle.

        The function takes the puzzle input as argument and should return a
        solution.

        Example:
            >>> puzzle = Puzzle(title="should be two")
            >>> @puzzle.solution
            ... def get_two():
            ...     return 2
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
            solution = solve_step()

            solutions.append(PuzzleSolution(
                str(solution) if solution is not None
                else None
            ))

        return solutions
