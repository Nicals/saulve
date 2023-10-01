import pytest

from saulve.errors import PuzzleHasNoSolution
from saulve.puzzle import Puzzle


def test_cannot_solve_puzzle_without_registered_solution() -> None:
    puzzle = Puzzle(name='Test Puzzle')

    with pytest.raises(PuzzleHasNoSolution):
        puzzle.solve()


def test_solve_puzzle_steps() -> None:
    puzzle = Puzzle(name='Test Puzzle')
    puzzle.solution(lambda: 12)

    solutions = puzzle.solve()

    assert len(solutions) == 1
    assert solutions[0].solution == '12'


def test_injects_puzzle_input() -> None:
    puzzle = Puzzle(name='Test puzzle')

    @puzzle.solution
    @puzzle.with_input('foobar')
    def solution(puzzle_input) -> str:
        return puzzle_input

    solutions = puzzle.solve()

    assert len(solutions) == 1
    assert solutions[0].solution == 'foobar'
