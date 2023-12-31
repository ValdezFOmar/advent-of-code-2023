from collections import Counter
from typing import Literal, Sequence, TypeAlias

import utils.iterutils as itu
from aoc.tools import YieldStr, run_challenge
from utils.matrix import transpose

Platform: TypeAlias = Sequence[Sequence[str]]
TiltDirection: TypeAlias = Literal["n", "w", "s", "e"]


def parse_input(input: YieldStr) -> list[tuple[str, ...]]:
    platform: list[tuple[str, ...]] = []
    for line in input:
        platform.append(tuple(line))
    return platform


def tilt_platform(platform: Platform, direction: TiltDirection) -> list[tuple[str, ...]]:
    transformed = False
    if direction == "n":
        reverse = True
        platform = transpose(platform)
        transformed = True
    elif direction == "s":
        reverse = False
        platform = transpose(platform)
        transformed = True
    elif direction == "w":
        reverse = True
    elif direction == "e":
        reverse = False
    else:
        raise ValueError("direction should be one of 'nsew'")

    tilted_platform: list[tuple[str, ...]] = []
    cube_rock = "#"

    for line in platform:
        sub_sequences = itu.divide_by(cube_rock, line)
        sub_sequences = (sorted(sub, reverse=reverse) for sub in sub_sequences)
        tilted_column = itu.join_from_iter(sub_sequences, value=cube_rock)
        tilted_platform.append(tuple(tilted_column))

    if transformed:
        return transpose(tilted_platform)
    return tilted_platform


def spin_cycle(platform: Platform) -> list[tuple[str, ...]]:
    return tilt_platform(tilt_platform(tilt_platform(tilt_platform(platform, "n"), "w"), "s"), "e")


def calculate_load(platform: Platform) -> int:
    num_rows = len(platform)
    round_rock = "O"
    total_load = 0
    for i, row in enumerate(platform):
        rounded_rocks = Counter(row).get(round_rock, 0)
        total_load += rounded_rocks * (num_rows - i)
    return total_load


def solution_part_1(input: YieldStr) -> int:
    platform = parse_input(input)
    return calculate_load(tilt_platform(platform, "n"))


def solution_part_2(input: YieldStr) -> int:
    platform = parse_input(input)
    seen_states = {tuple(platform): 0}
    num_spins = 0

    while True:
        platform = spin_cycle(platform)
        num_spins += 1
        freezed_platform = tuple(platform)
        if freezed_platform in seen_states:
            break
        seen_states[freezed_platform] = num_spins

    total_spins = 1_000_000_000
    cycle_start = seen_states[freezed_platform]
    period = num_spins - cycle_start
    remaining_spins = (total_spins - cycle_start) % period

    for _ in range(remaining_spins):
        platform = spin_cycle(platform)

    return calculate_load(platform)


if __name__ == "__main__":
    run_challenge(solution_part_2, __file__, debug=True)
