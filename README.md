[![test](https://github.com/Nicals/saulve/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/Nicals/saulve/actions?query=workflow:test+event:push+branch:master)
[![Coverage Status](https://coveralls.io/repos/github/Nicals/saulve/badge.svg?branch=master&kill_cache=1)](https://coveralls.io/github/Nicals/saulve?branch=master)

Saulve
======

A framework for computer programming challenge.

For the moment, only [Advent of Code](https://adventofcode.com) is supported.

Usage
-----

A few terms need to be defined first.
A **challenge** is a source of programming puzzles (such as [Advent of code](https://adventofcode.com/).
A puzzle is a given problem within a challenge (such as [multiple of 3 or 5](https://projecteuler.net/problem=1) 
in [Project Euler](https://projecteuler.net/).

The following example will setup an environment to solve [Project Euler](https://projecteuler.net/)
puzzles.
Start with a python project to store your challenges and create an `euler` package in it.
The name of the `euler` can be anything you want.

```
my_challenges/
  __init__.py
  euler/
    __init__.py
```

*Saulve* discovers puzzle by scanning modules in the `euler` package.
Each module having a `puzzle` attribute that is an instance of `saulve.Puzzle` will be loaded.

```python
# file: my_challenges/euler/problem_001.py
from saulve import Puzzle

puzzle = Puzzle(name="Multiple of 3 or 5", puzzle_input=1000)
```

Solutions to puzzles are registered by decorating functions with `Puzzle.solution`.
Solution functions takes one argument that is the `puzzle_input` value passed to the Puzzle
constructor.

```python
# file: my_challenges/euler/problem_001.py

@puzzle.solution
def solve(limit):
    return 12
```

Last thing to do is to tell *Saulve* where to find this Euler challenge.
Saulve entry point is an `app` attribute at the root module of your package.
The `app` attribute must be an instance of `saulve.App`.

```python
# file: my_challenges/__init__.py
from saulve import App
from saulve.challenges.generic import GenericLoader
from . import euler

app = App()

app.register_challenge('euler', GenericLoader(euler))
```

The call to `register_challenge` tells *Saulve* that a challenge must be registered under the
*euler* name (can be anything, it does not need to match the *euler* package name).
The challenge are loaded from the `euler` package using a `GenericLoader` (challenge in a given
package, one puzzle per module as described above).

You are now ready to use the *Saulve* cli.
You need to tell *Saulve* where your `app` attribute is using the `--app` argument (or by setting a
`SAULVE_CHALLENGES` env variable).
Each puzzle is identified by its module name.

You can list all puzzles registered under a challenge:

```bash-session
$ saulve --app challenges euler list
```


To run the solutions functions of a given puzzle:

```bash-session
$ saulve --app challenges euler solve problem_001
Multiple of 3 or 5:
  233168
```

The first argument (`euler`) tells saulve that you want to use the `euler` registered challenge.


### Advent of code support

For advent of code, each puzzle must be in a module named after the puzzle day (ex: `day_06.py`).
A module puzzle must have a `puzzle` attribute and some registered solution steps.


```python
# file: my_challenges/advent_of_code/year_2022/day_01.py
from saulve import Puzzle

puzzle = Puzzle(name='Calorie Counting', puzzle_input='...')

@puzzle.solution
def solve_first_star(puzzle_input):
    return 121

@puzzle.solution
def solve_second_star(puzzle_input):
    retuirn 1932
```

You then need to tell *Saulve* to register your advent of code package using an `AdventOfCode`
loader.
This loader understand the *year/month* package.

```python
# file my_challenge/__init__.py
from saulve import App
from saulve.challenges.advent_of_code import AdventOfCodeLoader
from . import advent_of_code

app = App()

app.register_challenge('aoc', AdventOfCodeLoader(advent_of_code))
```

You can now solve your challenge as before:

```bash-session
$ saulve --app my_challenges aoc solve 2022 01
Calorie Counting:
  121
  1932
```
