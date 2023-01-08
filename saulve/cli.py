from typing import Optional

import click

from .app import App, import_app
from .errors import PuzzleNotFound, ValidationError


def display_challenges(app: App) -> None:
    click.echo('Available challenges:')
    for challenge_name in app.loaders:
        click.echo(f'  {challenge_name}')


@click.group(invoke_without_command=True)
@click.option(
    '-a', '--app',
    'app_module',
    required=True,
    envvar='SAULVE_CHALLENGES',
    help='Application module.',
)
@click.argument('chall', required=False)
@click.pass_context
def cli(ctx: click.Context, app_module: str, chall: Optional[str]) -> None:
    ctx.ensure_object(dict)
    app = import_app(app_module)

    if chall is None:
        display_challenges(app)
        return

    challenge = app.get_challenge(chall)
    ctx.obj['CHALLENGE'] = challenge


@cli.command(name='list', help='List all puzzles.')
@click.argument('filters', nargs=-1)
@click.pass_context
def list_puzzles(ctx: click.Context, filters: list[str]) -> None:
    """List all puzzles in the selected challenge."""
    challenge = ctx.obj['CHALLENGE']

    for puzzle in challenge.find():
        click.echo(puzzle.name)


@cli.command(help='Solve a given puzzle.')
@click.argument('puzzle_id', nargs=-1, required=True)
@click.pass_context
def solve(ctx: click.Context, puzzle_id: list[str]) -> None:
    """Solve a puzzle in the selected challenge."""
    challenge = ctx.obj['CHALLENGE']

    try:
        puzzle = challenge.get(*puzzle_id)
    except ValidationError as e:
        raise click.ClickException(f'Invalid puzzle id. {e}')
    except PuzzleNotFound:
        raise click.ClickException('Puzzle not found.')

    solutions = puzzle.solve()

    click.echo(f'{puzzle.name}:')
    for solution in solutions:
        click.echo('  ', nl=False)
        click.echo(solution.solution if solution.is_solved else 'unsolved')
