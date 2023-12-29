import pytest

from aoc.tools import relative_test_file

from .challenge import read_until_comma, solution_part_1, solution_part_2


@pytest.mark.parametrize(
    "solution, output",
    [
        (solution_part_1, 1320),
        (solution_part_2, 145),
    ],
)
def test_solution(solution, output):
    assert solution(relative_test_file(__file__, reader=read_until_comma)) == output
