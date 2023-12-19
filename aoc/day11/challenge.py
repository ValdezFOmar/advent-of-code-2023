from __future__ import annotations

import re
from itertools import combinations
from typing import Iterable, NamedTuple

import utils.iterutils as itu
from aoc.tools import YieldStr, run_challenge


class Point(NamedTuple):
    row: int
    column: int

    def manhattan_distance(self, point: Point, /) -> int:
        return self.horizontal_distance(point) + self.vertical_distance(point)

    def horizontal_distance(self, point: Point, /) -> int:
        return abs(self.row - point.row)

    def vertical_distance(self, point: Point, /) -> int:
        return abs(self.column - point.column)


galaxy_finder = re.compile(r"#").finditer


def parse_input(input: YieldStr) -> tuple[list[Point], set[int], set[int]]:
    expand_columns = set[int]()
    expand_rows = set[int]()
    galaxies_coords: list[Point] = []

    for row, line in enumerate(input):
        galaxies = [Point(row, galaxy.start()) for galaxy in galaxy_finder(line)]
        galaxies_coords.extend(galaxies)

        if not expand_columns:
            expand_columns = set(range(len(line)))

        if not galaxies:
            expand_rows.add(row)
            continue

        expand_columns.difference_update(g.column for g in galaxies)
    return galaxies_coords, expand_rows, expand_columns


def expansion_between_points(
    p1: Point,
    p2: Point,
    rows: set[int],
    columns: set[int],
    expansion_factor=2,
) -> int:
    rows_between = itu.length_range(
        p1.row if p1.row < p2.row else p2.row, p1.horizontal_distance(p2)
    )
    columns_between = itu.length_range(
        p1.column if p1.column < p2.column else p2.column, p1.vertical_distance(p2)
    )

    # To only count the number of new rows/columns, without counting the ones that already exists
    expansion_factor -= 1

    num_expanded_rows = len(rows.intersection(rows_between)) * expansion_factor
    num_expanded_columns = len(columns.intersection(columns_between)) * expansion_factor
    return num_expanded_rows + num_expanded_columns


def solution_part_1(input: YieldStr) -> int:
    galaxies_coords, rows, columns = parse_input(input)
    sum_of_distances = 0

    for p1, p2 in combinations(galaxies_coords, 2):
        distance = p1.manhattan_distance(p2)
        expansion = expansion_between_points(p1, p2, rows, columns)
        sum_of_distances += distance + expansion

    return sum_of_distances


def solution_part_2(input: YieldStr) -> int:
    return 0


if __name__ == "__main__":
    run_challenge(solution_part_1, __file__, debug=True)
