from typing import Callable

import pytest

from saulve.errors import PuzzleHasNoSolution, WrongStepSolution
from saulve.puzzle.core import Puzzle, PuzzleStep


def _raise_wrong_step_solution() -> None:
    raise WrongStepSolution('Raised on purpose.')


def test_push_next_puzzle_step() -> None:
    root = PuzzleStep(lambda: 12)
    second = root.push_step(lambda: 12)
    third = root.push_step(lambda: 12)

    assert root._next is second
    assert root._next._next is third

    assert root.has_next is True
    assert second.has_next is True
    assert third.has_next is False


def test_execute_all_step_functions() -> None:
    step = PuzzleStep(lambda: 'first')
    step.push_step(lambda: 'second')

    solutions = step.run()

    assert len(solutions) == 2
    assert solutions[0].solution == 'first'
    assert solutions[1].solution == 'second'


@pytest.mark.parametrize('fn, expected_correctness', [
    (lambda: 12, True),
    (lambda: None, None),
    (_raise_wrong_step_solution, False),
])
def test_resolve_step_run_correctness(
    fn: Callable[[], str | None],
    expected_correctness: bool | None,
) -> None:
    step = PuzzleStep(fn)

    solutions = step.run()

    assert len(solutions) == 1
    assert solutions[0].is_correct is expected_correctness


def test_cannot_solve_puzzle_without_registered_solution() -> None:
    puzzle = Puzzle(name='Test Puzzle')

    with pytest.raises(PuzzleHasNoSolution):
        puzzle.solve()


def test_solve_puzzle_steps() -> None:
    puzzle = Puzzle(name='Test Puzzle')
    puzzle.solution(lambda: 12)
    puzzle.solution(lambda: 'second one')

    solutions = puzzle.solve()

    assert len(solutions) == 2
    assert solutions[0].solution == '12'
    assert solutions[1].solution == 'second one'
