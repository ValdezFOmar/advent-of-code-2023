import pytest

from aoc.tools import relative_test_file

from .challenge import solution_part_1, solution_part_2


@pytest.mark.parametrize(
    "solution, output",
    [
        (solution_part_1, 136),
        (solution_part_2, 0),
    ],
)
def test_solution(solution, output):
    assert solution(relative_test_file(__file__)) == output
