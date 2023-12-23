import pytest

from aoc.tools import relative_test_file

from .challenge import solution_part_1, solution_part_2


@pytest.mark.parametrize(
    "solution, output, file_name",
    [
        (solution_part_1, 32_000_000, "test-input-1.txt"),
        (solution_part_1, 11_687_500, "test-input-2.txt"),
        (solution_part_2, 0, "test-input-2.txt"),
    ],
)
def test_solution(solution, output, file_name):
    assert solution(relative_test_file(__file__, name=file_name)) == output
