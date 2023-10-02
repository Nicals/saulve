"""A generic challenge loader.

The challenges is a python package. Each module of this package containing a
'puzzle' attribute is loaded.
"""

import logging
import re
import types
from pathlib import Path
from typing import Optional

from saulve.errors import MissingAttribute, PuzzleNotFound, ValidationError
from saulve.import_module import import_instance
from saulve.puzzle import Puzzle

from .base import Challenge as BaseChallenge
from .base import ChallengeLoader, PuzzleView

logger = logging.getLogger(__name__)


class Challenge(BaseChallenge):
    def __init__(self, puzzles: dict[str, Puzzle]) -> None:
        self.puzzles = puzzles

    def find(self) -> list[PuzzleView]:
        return [
            PuzzleView(id=key, name=puzzle.name)
            for key, puzzle in self.puzzles.items()
        ]

    def get(self, *args: str) -> Puzzle:
        if len(args) != 1:
            raise ValidationError(f'1 id argument expected, got {len(args)}.')

        puzzle_id = args[0]

        try:
            return self.puzzles[puzzle_id]
        except KeyError as e:
            raise PuzzleNotFound(f"Puzzle '{puzzle_id}' not found.") from e


class GenericLoader(ChallengeLoader):
    def __init__(
        self,
        challenge_module: types.ModuleType,
        id_regexp: Optional[str] = None,
    ) -> None:
        """
        Arguments:
            challenge_module: The module to load puzzle from
            id_regexp: An optional regexp to use to extract an identifier from
                loaded puzzle name. If not set or if the regexp does not match,
                the puzzle module name will set as id.
        """
        self.challenge_module = challenge_module
        self.id_regexp = (
            re.compile(id_regexp) if id_regexp is not None else None
        )

    def _generate_puzzle_id(self, puzzle_module_name: str) -> str:
        puzzle_module = puzzle_module_name.split('.')[-1]

        if self.id_regexp is None:
            return puzzle_module

        if (m := self.id_regexp.search(puzzle_module)) is None:
            return puzzle_module

        try:
            return m.group(0)
        except IndexError:
            return puzzle_module

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

            puzzle_id = self._generate_puzzle_id(puzzle_module_name)
            if puzzle_id in puzzles:
                logger.warning(
                    f'Duplicated puzzle id \'{puzzle_id}\' in '
                    f'{puzzle_module_name}'
                )
            puzzles[puzzle_id] = puzzle

        return Challenge(puzzles)
