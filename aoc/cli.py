from pathlib import Path

import click

from .calendar import Calendar
from .errors import PuzzleInputMissing, PuzzleNotFound, SolutionModuleError


@click.group()
@click.option(
    '-p', '--puzzles',
    'puzzle_path',
    required=True,
    type=click.Path(
        exists=True,
        file_okay=False,
        resolve_path=True,
        path_type=Path,
    ),
    envvar='AOC_PUZZLES',
    help='Path to the puzzle directory.',
)
@click.pass_context
def cli(ctx, puzzle_path: Path):
    ctx.ensure_object(dict)

    try:
        ctx.obj['CALENDAR'] = Calendar(puzzle_path)
    except SolutionModuleError as e:
        raise click.ClickException(str(e))


@cli.command(help='List all known puzzles')
@click.option('-y', '--year', help='Show only puzzle of this year.')
@click.pass_context
def list(ctx, year: int | None) -> None:
    calendar = ctx.obj['CALENDAR']

    puzzles = calendar.list_puzzles(year=year)

    if puzzles:
        for puzzle in puzzles:
            click.echo(f'{puzzle.year}: {puzzle.day}')
    else:
        click.echo('No puzzle found')


@cli.command(help='Run a single puzzle.')
@click.argument('year', type=click.INT)
@click.argument('day', type=click.INT)
@click.pass_context
def run(ctx, year: int, day: int) -> None:
    calendar = ctx.obj['CALENDAR']

    try:
        puzzle = calendar.get_puzzle(year, day)
    except PuzzleNotFound:
        raise click.ClickException('Puzzle does not exist.')

    try:
        result = puzzle.run()
    except PuzzleInputMissing:
        raise click.ClickException('Puzzle input is missing.')

    if result.first_star.is_solved:
        click.echo(f'First star: {result.first_star.solution}')
    else:
        click.echo('First star: Not solved')

    if result.second_star.is_solved:
        click.echo(f'Second star: {result.second_star.solution}')
    else:
        click.echo('Second star: Not solved')
