from aoc.tools import run_challenge

from .challenge import read_until_comma, solution_part_1, solution_part_2

run_challenge(solution_part_1, relative_to=__file__, reader=read_until_comma)
run_challenge(solution_part_2, relative_to=__file__, reader=read_until_comma)
