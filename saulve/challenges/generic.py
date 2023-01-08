"""A generic challenge loader.

The challenges is a python package. Each module of this package containing a
'puzzle' attribute is loaded.
"""

from pathlib import Path
import types

from saulve.errors import MissingAttribute, PuzzleNotFound, ValidationError
from saulve.puzzle import Puzzle
from saulve.import_module import import_instance
from .base import Challenge as BaseChallenge, ChallengeLoader


class Challenge(BaseChallenge):
    def __init__(self, puzzles: dict[str, Puzzle]) -> None:
        self.puzzles = puzzles

    def find(self) -> list[Puzzle]:
        return list(self.puzzles.values())

    def get(self, *args: str) -> Puzzle:
        if len(args) != 1:
            raise ValidationError(f'1 id argument expected, got {len(args)}.')

        puzzle_id = args[0]

        try:
            return self.puzzles[puzzle_id]
        except KeyError:
            raise PuzzleNotFound(f"Puzzle '{puzzle_id}' not found.")


class GenericLoader(ChallengeLoader):
    def __init__(self, challenge_module: types.ModuleType) -> None:
        self.challenge_module = challenge_module

    def load(self) -> Challenge:
        puzzles: dict[str, Puzzle] = {}

        assert self.challenge_module.__file__ is not None
        challenge_path = Path(self.challenge_module.__file__).parent

        for filename in challenge_path.iterdir():
            if not filename.is_file():
                continue

            if filename.suffix != '.py':
                continue

            puzzle_module_name = '.'.join([
                self.challenge_module.__name__,
                filename.with_suffix('').name,
            ])

            try:
                puzzle = import_instance(puzzle_module_name, 'puzzle', Puzzle)
            except MissingAttribute:
                continue
            puzzles[filename.with_suffix('').name] = puzzle

        return Challenge(puzzles)
