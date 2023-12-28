import pytest

from aoc.tools import relative_test_file

from .challenge import solution_part_1, solution_part_2


@pytest.mark.parametrize(
    "solution, output, file_name",
    [
        (solution_part_1, 4, "test-input-1.txt"),
        (solution_part_1, 8, "test-input-2.txt"),
        (solution_part_2, 1, "test-input-1.txt"),
        (solution_part_2, 1, "test-input-2.txt"),
        (solution_part_2, 4, "test-input-3.txt"),
        (solution_part_2, 8, "test-input-4.txt"),
        (solution_part_2, 10, "test-input-5.txt"),
    ],
)
def test_solution(solution, output, file_name):
    assert solution(relative_test_file(__file__, name=file_name)) == output
