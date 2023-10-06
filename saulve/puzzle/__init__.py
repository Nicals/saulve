"""A puzzle holds  a list of solution steps. A puzzle is said to be solved if
all steps return an answer.

Puzzle steps are functions that return a response (int or str) or None if not
already solved.
Puzzle steps are registered in a puzzle by decorating them with the Puzzle.solution
decorator.

>>> from saulve import Puzzle, solved, with_input
>>> puzzle = Puzzle(name='An example puzzle')
>>> @puzzle.solution
... def solve_me():
...     return 'a solution'
...
>>> @puzzle.solution
... def unsolved():
...     return None
...
>>> puzzle.solve()
[
    PuzzleSolution(solution='a solution', is_correct=True),
    PuzzleSolution(solution=None, is_correct=None)
]

Some decorators are provided to alter the solutions behaviour.

The with_input decorator injects an initial value as first argument of the solution
step function.

>>> @puzzle.solution
>>> @with_input('some input')
>>> def solve_me(puzzle_input):
...    ...

The solved decorator will check if the returned solution is equal to the argument
passed to solved.
This decorator can be used as a unit test to refactor solutions steps.

>>> puzzle = Puzzle(name='A solved puzzle')
>>> @puzzle.solution
... @solved('expected answer')
... def solve_me():
...     return 'not the expected answer'
...
>>> puzzle.solve()
[PuzzleSolution(solution=None, is_correct=False)]
"""

from .core import Puzzle
from .decorators import solved, with_input

__all__ = ['Puzzle', 'solved', 'with_input']
