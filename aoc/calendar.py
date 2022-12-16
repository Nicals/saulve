"""
Fetches current puzzle state.

The puzzle directory must be a valid python package. Puzzle are sorted by
year, then by date.
Puzzle inputs are stored next to the `.py` files with a `.input` extension.

The puzzle directory should be organized in the following way:

    aoc_puzzles/
        __init__.py
        year_2022/
            __init__.py
            day_01.py
            day_01.input
"""

from importlib import import_module
import inspect
from pathlib import Path
import re
import sys

from .errors import PuzzleNotFound, SolutionModuleError
from .puzzle import Puzzle, Solution


__all__ = ['Calendar']


# expected names of puzzle solution files and directories
YEAR_REGEX = re.compile(r'^year_(?P<year>\d{4})$')
SOLUTION_FILE_REGEX = re.compile(r'day_(?P<day>\d{1,2})\.py$')


def import_solution(module_name: str) -> Solution:
    """Load an instance of an aoc.puzzle.Solution from a given module.

    The module must contain one and only one subclass of Solution.

    Raises:
        PuzzleModuleError: If no Solution or more than one Solution subclass
            are defined in the given module.
    """
    module = import_module(module_name)

    solutions = inspect.getmembers(
        module,
        lambda m: (
            inspect.isclass(m)
            and issubclass(m, Solution)
            and m != Solution
        )
    )

    if not solutions:
        raise SolutionModuleError(
            f"No '{Solution}' class found in '{module_name}'"
        )
    if len(solutions) != 1:
        raise SolutionModuleError(
            f"More than one '{Solution.__name__}' class in '{module_name}'"
        )

    return solutions[0][1]()


def mount_package_directory(path: Path) -> None:
    """
    Add `path` parent directory to the python path if not already present.
    """
    package_path = path.resolve().parent

    for python_path in sys.path:
        python_path = Path(python_path)
        #  I could not find if python path are resolved by default. It seems
        # they are but didn't find confirmation about this (did not want to
        # search this for hours though)...
        # So to be sure not to break anything, I resolve it second time.
        # Feel free to remove this line if you can confirm PYTHON_PATHs
        # resolvation (is this even a word ??).
        python_path.resolve()

        if not python_path.exists():
            continue

        if python_path.samefile(package_path):
            return

    sys.path.append(str(package_path.absolute()))


def load_puzzles(path: Path) -> list[Puzzle]:
    """
    Parse puzzle solution directory, imports puzzles it contains into Puzzle
    instances.

    Raises:
        PuzzleModuleError: If it fails to import a solution.
    """
    puzzles = []
    mount_package_directory(path)

    for year_dir in filter(lambda p: p.is_dir(), path.iterdir()):
        if (m := YEAR_REGEX.match(year_dir.name)) is None:
            continue

        year = m.group('year')

        for solution_file in filter(lambda p: p.is_file(), year_dir.iterdir()):
            if (m := SOLUTION_FILE_REGEX.match(solution_file.name)) is None:
                continue

            day = m.group('day')
            input_path = solution_file.with_suffix('.input')
            module_name = str(
                solution_file.relative_to(path.parent).with_suffix('')
            ).replace('/', '.')

            solution = import_solution(module_name)

            puzzles.append(Puzzle(
                year=int(year),
                day=int(day),
                solution=solution,
                input_path=input_path if input_path.exists() else None,
            ))

    return puzzles


class Calendar:
    """
    Arguments:
        path (Path): Directory to the puzzle directory

    Raises:
        PuzzleModuleError: If some puzzle solution failed to load.
        ValueError: If the path is not valid
    """
    def __init__(self, path: Path) -> None:
        if not path.exists():
            raise ValueError(f'{path} does not exist')

        if not path.is_dir():
            raise ValueError(f'{path} is not a directory')

        self.puzzles = load_puzzles(path)

    def list_puzzles(self, year: int | None) -> list[Puzzle]:
        """
        Get all puzzles.

        Arguments:
            year (int | None): If not None, will only list puzzles of this
                year.
        """
        return [p for p in self.puzzles if year is None or p.year == year]

    def get_puzzle(self, year: int, day: int) -> Puzzle:
        """
        Get a single puzzle.

        Raise:
            PuzzleNotFound: If the puzzle could not be found.
        """
        for puzzle in self.puzzles:
            if puzzle.year == year and puzzle.day == day:
                return puzzle

        raise PuzzleNotFound()
