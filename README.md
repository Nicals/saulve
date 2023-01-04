Advent Of Code
==============

A framework for computer programming challenge.

For the moment, only [Advent of Code](https://adventofcode.com) is supported.

Usage
-----

A few terms need to be defined first.
A **challenge** is a source of programming puzzle (such as [Advent of code](https://adventofcode.com/).
A puzzle is a given problem within a challenge (such as [multiple of 3 or 5](https://projecteuler.net/problem=1) 
in [Project Euler](https://projecteuler.net/).

For advent of code, each puzzle must be in a module named after the puzzle day (ex: `day_06.py`).
A module puzzle must have a `puzzle` attribute and some registered solution steps.


```python
# file: my_challenges/advent_of_code/year_2022/day_01.py
from aoc import Puzzle

puzzle = Puzzle(name='Calorie Counting', puzzle_input='...')

@puzzle.solution
def solve_first_star(puzzle_input):
  ...

@puzzle.solution
def solve_second_star(puzzle_input):
  ...
```

To make AOC aware of the advent of code puzzle, an application instance must be created and the
advent of code challenge registered into it.

```python
# file my_challenge/__init__.py
from aoc import App
from aoc.challenges.advent_of_code import AdventOfCodeLoader
from . import advent_of_code

app = App()

app.register_challenge('my-aoc-challenge', AdventOfCodeLoader(advent_of_code))
```

The aoc cli can now be used to solve challenges.
The module containing the `App` instance created above must be given as an `--app` argument (or in a
`AOC_CHALLENGES` environment variable).

```bash-session
$ aoc --app challenges my-aoc-challenge solve 2022 01
Calorie Counting:
  121
  1932
```
