import logging
from unittest.mock import Mock

import pytest

from saulve.challenges.generic import Challenge, GenericLoader
from saulve.errors import PuzzleNotFound, ValidationError
from saulve.puzzle import Puzzle

from .fixtures import generic as generic_fixtures


class TestChallenge:
    def test_validates_get_puzzle_arg_count(self) -> None:
        chall = Challenge(puzzles={})
        expected_msg = r'1 id argument expected, got 2'

        with pytest.raises(ValidationError, match=expected_msg):
            chall.get('foo', 'bar')

    def test_get_unexisting_puzzle_raises_exception(self) -> None:
        chall = Challenge(puzzles={})

        with pytest.raises(PuzzleNotFound):
            chall.get('foo')

    def test_get_challenge(self) -> None:
        puzzle = Mock(Puzzle)
        chall = Challenge(puzzles={'foo': puzzle})

        retrieved_puzzle = chall.get('foo')

        assert retrieved_puzzle is puzzle

    def test_finds_challenges(self) -> None:
        puzzle = Mock(Puzzle)
        puzzle.name = 'Puzzle name'
        chall = Challenge(puzzles={'foo': puzzle})

        found_puzzles = chall.find()

        assert len(found_puzzles) == 1
        assert found_puzzles[0].id == 'foo'
        assert found_puzzles[0].name == 'Puzzle name'


class TestGenericLoader:
    def test_loads_challenges(self) -> None:
        loader = GenericLoader(generic_fixtures)

        chall = loader.load()

        assert 'contains_puzzle' in chall.puzzles
        assert chall.puzzles['contains_puzzle'].name == 'A puzzle'

    def test_extract_puzzle_id_from_regexp(self) -> None:
        loader = GenericLoader(generic_fixtures, id_regexp=r'(contains)')

        chall = loader.load()

        assert 'contains' in chall.puzzles
        assert chall.puzzles['contains'].name == 'A puzzle'

        assert 'other_puzzle' in chall.puzzles
        assert chall.puzzles['other_puzzle'].name == 'Other puzzle'

    def test_warn_about_duplicated_puzzle_id(self, caplog) -> None:
        loader = GenericLoader(generic_fixtures, id_regexp=r'(puzzle)')

        with caplog.at_level(logging.WARNING, logger='saulve.challenge.generic'):
            loader.load()

        assert (
            "Duplicated puzzle id 'puzzle' in tests.challenges.fixtures.generic.contains_puzzle"
            in caplog.text
        )
