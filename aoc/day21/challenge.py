from functools import partial
from typing import Iterator, Sequence

from aoc.tools import YieldStr, run_challenge
from utils.iterutils import get_index
from utils.matrix import Direction
from utils.matrix import Vector as Point

Garden = Sequence[str]


def parse_input(input: YieldStr) -> tuple[Garden, Point]:
    garden: list[str] = []
    starting_position = None
    for row, line in enumerate(input):
        if (column := get_index(line, "S")) is not None:
            starting_position = Point(row, column)
            line = line.replace("S", ".")
        garden.append(line)
    assert starting_position is not None
    return garden, starting_position


def posible_steps(garden: Garden, position: Point) -> Iterator[Point]:
    row_limits = range(len(garden))
    column_limits = range(len(garden[0]))
    for direction in Direction:
        next_step = position + direction
        if not (next_step.row in row_limits and next_step.column in column_limits):
            continue
        tile = garden[next_step.row][next_step.column]
        if tile == "#":
            continue
        yield next_step


def solution_part_1(input: YieldStr, steps: int) -> int:
    garden, start_pos = parse_input(input)
    current_positions: set[Point] = {start_pos}
    next_positions: set[Point] = set()

    for _ in range(steps):
        for position in current_positions:
            posible_positions = posible_steps(garden, position)
            next_positions.update(posible_positions)
        current_positions = next_positions
        next_positions = set()

    return len(current_positions)


def solution_part_2(input: YieldStr) -> int:
    return 0


if __name__ == "__main__":
    run_challenge(partial(solution_part_1, steps=6), __file__, debug=True)
