import functools

from aoc.tools import run_challenge

from .challenge import solution_part_1, solution_part_2

run_challenge(functools.partial(solution_part_1, steps=64), relative_to=__file__)
run_challenge(solution_part_2, relative_to=__file__)
