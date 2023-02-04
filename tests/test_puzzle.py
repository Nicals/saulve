import pytest

from saulve.errors import PuzzleHasNoSolution
from saulve.puzzle import Puzzle


def test_cannot_solve_puzzle_without_registered_solution() -> None:
    puzzle = Puzzle[None](name='Test Puzzle')

    with pytest.raises(PuzzleHasNoSolution):
        puzzle.solve()


def test_solve_puzzle_steps() -> None:
    puzzle = Puzzle[int](name='Test Puzzle')
    puzzle.solution(lambda _: 12)

    solutions = puzzle.solve()

    assert len(solutions) == 1
    assert solutions[0].solution == '12'
