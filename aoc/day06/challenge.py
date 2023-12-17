import functools
import math
import re
import sys
from dataclasses import dataclass
from typing import Iterator

YieldStr = Iterator[str]


@dataclass
class Race:
    time: int
    distance_record: int

    @property
    def optimal_time(self) -> float:
        """Find the time for which boat would travel the farthest.
        Implemented using the `Vertex Formula` for a cuadratic equation.
        """
        a, b = -1, self.time
        x = -b / (2 * a)
        return x

    def boat_time(self, distance: float) -> tuple[float, float]:
        """Times that the button needs to be pressed to reach the given `distance`."""
        # Find the `x` value for given `y` in a cuadratic formula
        # Uses the cuadratic equation
        a, b, c = -1, self.time, -distance

        discriminant = b**2 - (4 * a * c)
        sqrt = math.sqrt(discriminant)
        time1 = (-b + sqrt) / (2 * a)
        time2 = (-b - sqrt) / (2 * a)

        return (time1, time2) if time1 < time2 else (time2, time1)

    def boat_distance(self, seconds: int):
        """Distance the boat would travel after pressing the button by `seconds`."""
        remaining_time = self.time - seconds
        return remaining_time * seconds


def ilen(iterable: Iterator[object]) -> int:
    """Return the iterator length."""
    return functools.reduce(lambda sum, _: sum + 1, iterable, 0)


def read_lines_from_file(path):
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            yield line


def parse_input(input: YieldStr) -> Iterator[Race]:
    numbers = re.compile(r"\d+")
    times = [int(num) for num in numbers.findall(next(input))]
    distances = [int(num) for num in numbers.findall(next(input))]
    races = (
        Race(time, distance) for time, distance in zip(times, distances, strict=True)
    )
    return races


TEST_INPUT = """\
Time:      7  15   30
Distance:  9  40  200
"""


def part_1(input: YieldStr, testing: bool):
    TEST_OUTPUT = 288

    races = parse_input(input)
    accumulator = 1

    for race in races:
        distances = (race.boat_distance(seconds) for seconds in range(race.time + 1))
        distances = (dist for dist in distances if dist > race.distance_record)
        accumulator *= ilen(distances)

    print(accumulator)

    if testing:
        assert accumulator == TEST_OUTPUT


def part_2(input: YieldStr, testing: bool):
    time = int("".join(next(input).split(":")[1].split()))
    dist = int("".join(next(input).split(":")[1].split()))
    race = Race(time, dist)

    x1, x2 = race.boat_time(dist)
    left_bound = math.ceil(x1)
    right_bound = math.floor(x2)
    nums_ways_win = right_bound - left_bound + 1  # +1: Also count the left bound itself

    print(nums_ways_win)

    if testing:
        TEST_OUTPUT = 71503
        assert nums_ways_win == TEST_OUTPUT


def main():
    testing = False
    if len(sys.argv) < 2:
        input = (line for line in TEST_INPUT.splitlines())
        testing = True
    else:
        input = read_lines_from_file(sys.argv[1])
    # part_1(input, testing)
    part_2(input, testing)


if __name__ == "__main__":
    main()
