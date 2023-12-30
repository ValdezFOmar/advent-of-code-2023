from aoc.tools import relative_input_file_path, relative_test_file

from .challenge import solution_part_1, solution_part_2


def test_solution_1():
    assert solution_part_1(relative_test_file(__file__)) == 46


def test_solution_2():
    assert solution_part_2(relative_input_file_path(__file__)) == 51
