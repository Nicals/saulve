"""Declare puzzle and their associated solution.
"""

from typing import Callable, NamedTuple

from ..errors import PuzzleHasNoSolution, WrongStepSolution
from .common import PuzzleStepResult

__all__ = ['Puzzle']


class PuzzleSolution(NamedTuple):
    """
    The result of one stage of a puzzle.
    """
    solution: str | None
    is_correct: bool | None

    @property
    def is_solved(self) -> bool:
        return self.solution is not None


class PuzzleStep:
    """A linked linked of solution step functions.

    The solution function can either return a response or None. A None return
    value is considered a solution without implemented response.
    """
    def __init__(self, fn: Callable[[], PuzzleStepResult]):
        self.fn = fn
        self._next: PuzzleStep | None = None

    def push_step(self, fn: Callable[[], PuzzleStepResult]) -> 'PuzzleStep':
        """Add a new solution function step at the end of the structure.
        """
        if self._next is not None:
            return self._next.push_step(fn)

        self._next = PuzzleStep(fn)
        return self._next

    @property
    def has_next(self) -> bool:
        return self._next is not None

    def run(self) -> list[PuzzleSolution]:
        """Run the step solution functions of this step and the next ones.
        """
        solution = None
        is_correct = None

        try:
            solution = self.fn()
        except WrongStepSolution:
            is_correct = False
        else:
            is_correct = None if solution is None else True

        return [
            PuzzleSolution(
                solution=str(solution) if solution is not None else None,
                is_correct=is_correct,
            )
        ] + (self._next.run() if self._next else [])


class Puzzle:
    """Holds solutions of a puzzle and its input data.

    Some solution functions steps are registered by decorating them with
    the `solution` decorator.

    Arguments:
        name: A verbose name for this puzzle

    Attributes:
        name: A verbose title for the current puzzle
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self._steps: PuzzleStep | None = None

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: {self.name}>'

    def __str__(self) -> str:
        return self.name

    def solution(
        self,
        fn: Callable[[], PuzzleStepResult],
    ) -> PuzzleStep:
        """Register a solution function for the puzzle.

        The function takes the puzzle input as argument and should return a
        solution.

        Example:
            >>> puzzle = Puzzle(title="should be two")
            >>> @puzzle.solution
            ... def get_two():
            ...     return 2
        """
        if self._steps is None:
            self._steps = PuzzleStep(fn)
            return self._steps

        return self._steps.push_step(fn)

    def solve(self) -> list[PuzzleSolution]:
        """Run all registered solutions for this puzzle and return a list of
        solution values.

        Raises:
            PuzzleHasNoSolution: If no solution have been registered for this
                puzzle.
        """
        if self._steps is None:
            raise PuzzleHasNoSolution(
                f"{self} don't have registered solutions"
            )

        return self._steps.run()
