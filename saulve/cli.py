import click

from .app import import_app
from .errors import PuzzleNotFound, ValidationError


@click.group()
@click.option(
    '-a', '--app',
    'app_module',
    required=True,
    envvar='SAULVE_CHALLENGES',
    help='Application module.',
)
@click.argument('chall')
@click.pass_context
def cli(ctx: click.Context, app_module: str, chall: str) -> None:
    ctx.ensure_object(dict)

    app = import_app(app_module)
    challenge = app.get_challenge(chall)

    ctx.obj['CHALLENGE'] = challenge


@cli.command(name='list', help='List all puzzles.')
@click.argument('filters', nargs=-1)
@click.pass_context
def list_puzzles(ctx: click.Context, filters: list[str]) -> None:
    """List all puzzles in the selected challenge."""
    click.echo(ctx.obj['CHALLENGE'])
    click.echo(filters)


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