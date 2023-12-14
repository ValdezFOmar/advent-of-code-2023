import pytest

from aoc.tools import relative_test_file

from .aoc_day5_part2 import solution_part_1, solution_part_2


@pytest.mark.parametrize(
    "solution, output",
    [
        (solution_part_1, 35),
        (solution_part_2, 0),
    ],
)
def test_solution(solution, output):
    assert solution(relative_test_file(__file__)) == output
