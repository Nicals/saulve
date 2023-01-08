from unittest.mock import Mock

from saulve.puzzle import Puzzle
from saulve.challenges.advent_of_code import AdventOfCodePuzzle, Calendar


class TestCalendar:
    def test_finds_challenges(self) -> None:
        puzzle = Mock(Puzzle)
        chall = Calendar([AdventOfCodePuzzle(2022, 1, puzzle)])

        found_puzzles = chall.find()

        assert found_puzzles == [puzzle]
