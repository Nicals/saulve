from click.testing import CliRunner

from saulve import App, Puzzle
from saulve.challenges.in_memory import InMemoryLoader
from saulve.cli import cli


puzzle = Puzzle(name='Test puzzle', puzzle_input='foo')
puzzle.solution(lambda a: 'bar')


app = App()
app.register_challenge('test-challenge', InMemoryLoader([puzzle]))


def test_list_challenges_if_no_challenge_given() -> None:
    runner = CliRunner()

    result = runner.invoke(cli, ['--app', __name__])

    assert result.exit_code == 0
    assert 'test-challenge' in result.output


def test_list_puzzles() -> None:
    runner = CliRunner()

    result = runner.invoke(cli, ['--app', __name__, 'test-challenge', 'list'])

    assert result.exit_code == 0
    assert '0 - Test puzzle' in result.output
