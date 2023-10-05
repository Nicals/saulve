"""Puzzle step function decorators.
"""

from functools import wraps
from typing import Callable, Concatenate, ParamSpec, TypeVar

from ..errors import WrongStepSolution
from .common import PuzzleStepResponse, PuzzleStepResult

U = TypeVar('U')

P = ParamSpec('P')


def with_input(puzzle_input: U) -> Callable[
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


def solved(solution: PuzzleStepResponse) -> Callable[
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
