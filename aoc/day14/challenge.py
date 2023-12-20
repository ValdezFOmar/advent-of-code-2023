from collections import Counter
from pprint import pprint
from typing import Iterator, TypeAlias

import utils.iterutils as itu
from aoc.tools import YieldStr, run_challenge
from utils import matrix

PLATFORM_OBJS = {".": 1, "O": 0, "#": 9}


Platform: TypeAlias = list[list[int]]


def parse_input(input: YieldStr) -> Platform:
    platform = []
    for line in input:
        platform.append([PLATFORM_OBJS[char] for char in line])
    return platform


def itilt_platform_north(platform: Platform) -> Iterator[tuple[int, ...]]:
    tilted_platform = []
    cube_rock = PLATFORM_OBJS["#"]

    for column in matrix.itranspose(platform):
        sub_sequences = itu.divide_by(cube_rock, column)
        sub_sequences = (sorted(sub) for sub in sub_sequences)
        tilted_column = itu.join_from_iter(sub_sequences, value=cube_rock)
        tilted_platform.append(tilted_column)

    return matrix.itranspose(tilted_platform)


def solution_part_1(input: YieldStr) -> int:
    platform = parse_input(input)
    num_rows = len(platform)
    round_rock = PLATFORM_OBJS["O"]

    total_load = 0

    for i, row in enumerate(itilt_platform_north(platform)):
        rounded_rocks = Counter(row).get(round_rock, 0)
        total_load += rounded_rocks * (num_rows - i)

    return total_load


def solution_part_2(input: YieldStr) -> int:
    return 0


if __name__ == "__main__":
    run_challenge(solution_part_1, __file__, debug=True)
