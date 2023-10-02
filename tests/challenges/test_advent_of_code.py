from unittest.mock import Mock

from saulve.challenges.advent_of_code import AdventOfCodePuzzle, Calendar
from saulve.puzzle import Puzzle


class TestCalendar:
    def test_finds_challenges(self) -> None:
        puzzle = Mock(Puzzle)
        puzzle.name = 'Puzzle name'
        chall = Calendar([AdventOfCodePuzzle(2022, 1, puzzle)])

        found_puzzles = chall.find()

        assert len(found_puzzles) == 1
        assert found_puzzles[0].id == '2022 01'
        assert found_puzzles[0].name == 'Puzzle name'
