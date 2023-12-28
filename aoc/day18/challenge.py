import re
from typing import Iterator

from aoc.tools import YieldStr, run_challenge
from utils import extra_math as xmath
from utils.matrix import Direction, Point

CHAR_TO_DIRECTION = {direct.name[0].upper(): direct for direct in Direction}


def parse_input(input: YieldStr) -> Iterator[tuple[str, int, str]]:
    parse_line = re.compile(r"([UDRL]) (\d+) \(#([0-9A-Fa-f]{6})\)")
    for line in input:
        match = parse_line.match(line)
        assert match is not None
        yield match[1], int(match[2]), match[3]


def solution_part_1(input: YieldStr) -> int:
    points: list[Point] = []
    last_point = Point(0, 0)

    for char, num, _ in parse_input(input):
        direction = CHAR_TO_DIRECTION[char]
        for _ in range(num):
            last_point += direction
            points.append(last_point)

    boundary = len(points)
    area = xmath.number_interior_points(xmath.shoelace_formula(points), boundary)
    return area + boundary


def solution_part_2(input: YieldStr) -> int:
    return 0


if __name__ == "__main__":
    run_challenge(solution_part_1, __file__, debug=True)
