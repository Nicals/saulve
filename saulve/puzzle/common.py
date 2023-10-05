"""Some common declarations for puzzles.
"""


# The response of a puzzle step.
PuzzleStepResponse = int | str

# Return value of a puzzle step. None indicates an unsolved step.
PuzzleStepResult = PuzzleStepResponse | None
