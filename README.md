Advent Of Code
==============

A framework for the [Advent of Code](https://adventofcode.com) challenge.


Usage
=====

You first need a puzzle repository.
Each puzzle solution is a `day_<int>.py` file in a `year_<int>` directory.
The location of the `year` folder must be a valid python package.
Puzzle input needs te be alongside the puzzle solution and named with a
`.input` extension.

For example:

```
/advent_of_code/
  __init__.py
  2022/
    __init__.py
    day_01.py
    day_01.input
```

A puzzle solution is a class extending `aoc.Soluton`.
The following method can be overriden:

  + `parse_input_file`: Receive le puzzle input file and prepare it for solving.
  + `first_star`: Receive the output of `parse_input_file` and returns the puzzle solution.
  + `second_star`: Same as above, but for second stage of the puzzle.


```python
from typing import IO
from aoc import Solution

PuzzleInput = list[int]

class MySolution(Solution[PuzzleInput]):
  def parse_input_file(self, file: IO[str]) -> PuzzleInput:
    return [int(e) for e in file.read()]

  def first_star(self, puzzle: PuzzleInput) -> int:
    return puzzle[0]
```

The `aoc` cli tool can then be used to list and run puzzle solutions.
The puzzle directory must be given either with a `--puzzle` arguments or by
setting an `AOC_PUZZLES` environment varialbe.

```bash-session
$ aoc --puzzle /path/to/puzzle list

# or

$ AOC_PUZZLES=/path/to/puzzle aoc list
```

The `run` command will execute a given solution and output its result.

```bash-session
$ aoc --puzzle run 2022 1
```
