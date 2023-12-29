import functools

import pytest

from aoc.tools import relative_test_file

from .challenge import general_solution


@pytest.mark.parametrize(
    "solution, output",
    [
        (functools.partial(general_solution, expansion_factor=2), 374),
        (functools.partial(general_solution, expansion_factor=10), 1030),
        (functools.partial(general_solution, expansion_factor=100), 8410),
    ],
)
def test_solution(solution, output):
    assert solution(relative_test_file(__file__)) == output
