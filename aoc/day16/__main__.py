from aoc.tools import run_challenge, run_challenge_with_path

from .challenge import solution_part_1, solution_part_2

run_challenge(solution_part_1, relative_to=__file__)
run_challenge_with_path(solution_part_2, relative_to=__file__)
