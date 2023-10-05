import pytest

from saulve.errors import WrongStepSolution
from saulve.puzzle.decorators import solved, with_input


@pytest.mark.parametrize('decorate', [
    solved(12),
    with_input(12),
])
def test_decorated_functions_are_wrapped(decorate) -> None:  # type: ignore
    def under_test() -> None:
        """Docstring"""

    decorated = decorate(under_test)

    assert decorated.__doc__ == 'Docstring'

def test_step_input_is_injected_as_first_argument() -> None:
    fn = with_input('Ministry of ')(lambda s: s + 'silly walks')

    assert fn() == 'Ministry of silly walks'


def test_solved_wont_do_anything_with_correct_solution() -> None:
    fn = solved('Tis but a scratch')(lambda: 'Tis but a scratch')

    assert fn() == 'Tis but a scratch'


def test_solved_raises_exception_on_wrong_solution() -> None:
    fn = solved('This parrot is dead.')(lambda: 'No, it\'s resting.')

    with pytest.raises(WrongStepSolution):
        fn()
