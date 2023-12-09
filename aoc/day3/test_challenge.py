from pathlib import Path

import pytest

from aoc.tools import read_lines_from_file

from .challenge import solution_part_1, solution_part_2

INPUT_PATH = Path(__file__).parent / "test-input.txt"


@pytest.mark.parametrize(
    "solution, input_path, output",
    [
        (solution_part_1, INPUT_PATH, 0),
        (solution_part_2, INPUT_PATH, 0),
    ],
)
def test_solution(solution, input_path, output):
    input = read_lines_from_file(input_path)
    assert solution(input) == output
