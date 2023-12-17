from pathlib import Path

import pytest

from aoc.tools import read_lines_from_file

from .challenge import solution_part_1, solution_part_2

PARENT_PATH = Path(__file__).parent


@pytest.mark.parametrize(
    "solution, input_path, output",
    [
        (solution_part_1, PARENT_PATH / "test-input-1.txt", 2),
        (solution_part_1, PARENT_PATH / "test-input-2.txt", 6),
        (solution_part_2, PARENT_PATH / "test-input-3.txt", 6),
    ],
)
def test_solution(solution, input_path, output):
    input = read_lines_from_file(input_path)
    assert solution(input) == output
