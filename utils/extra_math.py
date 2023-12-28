"""Module for implementing math formulas/theorems for use in solutions."""

import itertools
from functools import reduce
from typing import Sequence

from .matrix import Point


# https://en.wikipedia.org/wiki/Shoelace_formula#Example
def shoelace_formula(points: Sequence[Point]) -> float:
    """Get the area of a simple polygon by the coordinates of its vertices."""

    def _determinant(p1: Point, p2: Point) -> int:
        return (p1.x * p2.y) - (p1.y * p2.x)

    points_pairs = itertools.pairwise(itertools.chain(points, [points[0]]))
    doubled_area = reduce(lambda area, points: area + _determinant(*points), points_pairs, 0)
    return abs(doubled_area / 2)


# https://en.wikipedia.org/wiki/Pick%27s_theorem#Formula
def number_interior_points(area: float, num_boundary_points: int) -> int:
    """
    Number of points inside a simple polygon using Pick's theorem.

        A = i + b / 2 - 1  -->  i = A - b / 2 + 1

    A = area
    b = number of boundary points
    i = number of interior points (return value)
    """
    i = area - (num_boundary_points / 2) + 1
    return int(i)
