from functools import partial

import pytest

from aoc.tools import relative_test_file

from .challenge import solution_part_1, solution_part_2


@pytest.mark.parametrize(
    "solution, output",
    [
        (partial(solution_part_1, at_least=7, at_most=27), 2),
        (solution_part_2, 0),
    ],
)
def test_solution(solution, output):
    assert solution(relative_test_file(__file__)) == output
