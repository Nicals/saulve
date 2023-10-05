"""Declare puzzle and their associated solution.
"""

from functools import wraps
from typing import Callable, Concatenate, NamedTuple, ParamSpec, TypeVar

from .errors import PuzzleHasNoSolution, WrongStepSolution

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


# The response of a puzzle step.
PuzzleStepResponse = int | str
# Return value of a puzzle step. None indicates an unsolved step.
PuzzleStepResult = PuzzleStepResponse | None


T = TypeVar('T')
U = TypeVar('U')

P = ParamSpec('P')


class PuzzleStep:
    """A linked linked of solution step functions.
    """
    def __init__(self, fn: Callable[P, PuzzleStepResult]):
        self.fn = fn
        self._next: PuzzleStep | None = None

    def push_step(self, fn: Callable[P, PuzzleStepResult]) -> 'PuzzleStep':
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
        self._steps: PuzzleStep | None = None
        self.steps: list[Callable[[], PuzzleStepResult]] = []  # XXX: Remove this

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: {self.name}>'

    def __str__(self) -> str:
        return self.name

    def with_input(self, puzzle_input: U) -> Callable[
        [Callable[Concatenate[U, P], PuzzleStepResult]],
        Callable[P, PuzzleStepResult],
    ]:
        """Injects a value as first argument of the solution step function.
        """
        def decorator(
            fn: Callable[Concatenate[U, P], PuzzleStepResult],
        ) -> Callable[P, PuzzleStepResult]:
            @wraps(fn)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> PuzzleStepResult:
                return fn(puzzle_input, *args, **kwargs)

            return wrapper

        return decorator  # type: ignore[return-value] # pending issue 9


    def solved(self, solution: PuzzleStepResponse) -> Callable[
        [Callable[P, PuzzleStepResult]],
        Callable[P, PuzzleStepResult],
    ]:
        """Mark a solution function as solved. The return value of the solution
        function must match the passed argument to considere the response as
        correct.
        """
        def decorator(
            fn: Callable[P, PuzzleStepResult],
        ) -> Callable[P, PuzzleStepResult]:
            @wraps(fn)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> PuzzleStepResult:
                step_solution = fn(*args, **kwargs)

                if step_solution is not None and step_solution != solution:
                    raise WrongStepSolution()

                return step_solution

            return wrapper

        return decorator


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
