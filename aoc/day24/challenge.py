from dataclasses import dataclass
from functools import partial
from itertools import islice
from typing import NamedTuple, Self, Sequence

from aoc.tools import YieldStr, run_challenge
from utils.iterutils import find_numbers


class Vector3D(NamedTuple):
    x: float
    y: float
    z: float


@dataclass(slots=True, frozen=True)
class Line:
    m: float
    b: float

    @classmethod
    def from_point_vector(cls, p: Vector3D, v: Vector3D) -> Self:
        m = v.y / v.x
        b = p.y - m * p.x
        return cls(m, b)

    def f(self, x: float) -> float:
        return self.m * x + self.b

    def intersects(self, line: Self) -> bool:
        return self.intersection(line) is not None

    def intersection(self, line: Self) -> float | None:
        try:
            return (line.b - self.b) / (self.m - line.m)
        except ZeroDivisionError:
            return None


@dataclass(slots=True, frozen=True)
class Hailstone:
    position: Vector3D
    velocity: Vector3D

    def trayectory_intersection(self, other: Self) -> Vector3D | None:
        trayectory_1 = Line.from_point_vector(self.position, self.velocity)
        trayectory_2 = Line.from_point_vector(other.position, other.velocity)
        x_intersection = trayectory_1.intersection(trayectory_2)

        if x_intersection is None:
            return None

        y_intersection = trayectory_1.f(x_intersection)
        return Vector3D(x_intersection, y_intersection, 0)

    def is_past_position(self, position: Vector3D) -> bool:
        if self.velocity.y > 0:
            return self.position.y > position.y
        return self.position.y < position.y


def number_intersections(
    lower_limit: int,
    upper_limit: int,
    hailstones: Sequence[Hailstone],
) -> int:
    total_intersections = 0
    last_index = len(hailstones) - 1

    for i, hail_1 in enumerate(islice(hailstones, last_index), 1):
        for hail_2 in islice(hailstones, i, None):
            intersection = hail_1.trayectory_intersection(hail_2)
            if intersection is None:
                continue
            if not (
                lower_limit <= intersection.x <= upper_limit
                and lower_limit <= intersection.y <= upper_limit
            ):
                continue
            if hail_1.is_past_position(intersection) or hail_2.is_past_position(intersection):
                continue
            total_intersections += 1

    return total_intersections


def parse_input(input: YieldStr) -> list[Hailstone]:
    hailstones = []
    for line in input:
        pos, vel = line.split("@")
        pos = [int(num) for num in find_numbers(pos)]
        vel = [int(num) for num in find_numbers(vel)]
        hailstones.append(Hailstone(Vector3D(*pos), Vector3D(*vel)))
    return hailstones


def solution_part_1(input: YieldStr, at_least: int, at_most: int) -> int:
    hailstones = parse_input(input)
    return number_intersections(at_least, at_most, hailstones)


def solution_part_2(input: YieldStr) -> int:
    return 0


if __name__ == "__main__":
    run_challenge(partial(solution_part_1, at_least=7, at_most=27), __file__, debug=True)
