"""Advent of code challenge implementation
"""

import re
import types
from pathlib import Path
from typing import NamedTuple

from saulve import Puzzle
from saulve.errors import PuzzleNotFound, ValidationError
from saulve.import_module import import_instance

from .base import Challenge, ChallengeLoader, PuzzleView

YEAR_REGEX = re.compile(r'^year_(?P<year>\d{4})$')
PUZZLE_REGEX = re.compile(r'^day_(?P<day>\d{1,2})\.py$')


class AdventOfCodePuzzle(NamedTuple):
    year: int
    day: int
    puzzle: Puzzle

    def __repr__(self) -> str:
        return f'<{self.__class__}: {self.year}-{self.day:02}>'


class Calendar(Challenge):
    def __init__(self, puzzles: list[AdventOfCodePuzzle]) -> None:
        self.puzzles = puzzles

    def find(self) -> list[PuzzleView]:
        return [
            PuzzleView(
                id=f'{puzzle.year} {puzzle.day:02}',
                name=puzzle.puzzle.name,
            )
            for puzzle in self.puzzles
        ]

    def get(self, *args: str) -> Puzzle:
        if len(args) != 2:
            raise ValidationError('YEAR and DAY expected.')

        try:
            year = int(args[0])
        except ValueError as e:
            raise ValidationError(f"'{args[0]} is not a valid year.") from e

        try:
            day = int(args[1])
        except ValueError as e:
            raise ValidationError(f"'{args[1]} is not a valid day.") from e

        for puzzle in self.puzzles:
            if puzzle.year == year and puzzle.day == day:
                return puzzle.puzzle

        raise PuzzleNotFound(f'Puzzle {year} {day:02} not found.')


class AdventOfCodeLoader(ChallengeLoader):
    def __init__(self, challenge_module: types.ModuleType) -> None:
        self.challenge_module = challenge_module

    def load(self) -> Challenge:
        puzzles: list[AdventOfCodePuzzle] = []

        assert self.challenge_module.__file__ is not None
        challenge_path = Path(self.challenge_module.__file__).parent

        for year_dir in challenge_path.iterdir():
            if not year_dir.is_dir():
                continue

            if (m := YEAR_REGEX.match(year_dir.name)) is None:
                continue

            year = int(m.group('year'))

            for day_file in year_dir.iterdir():
                if not day_file.is_file():
                    continue

                if (m := PUZZLE_REGEX.match(day_file.name)) is None:
                    continue

                day = int(m.group('day'))

                puzzle_module = '.'.join([
                    self.challenge_module.__name__,
                    year_dir.name,
                    day_file.with_suffix('').name,
                ])
                puzzle = import_instance(puzzle_module, 'puzzle', Puzzle)

                puzzles.append(AdventOfCodePuzzle(year, day, puzzle))

        return Calendar(puzzles)
