""" Beaten B) """

import re
import sys
from dataclasses import dataclass
from enum import StrEnum

TEST_INPUT = """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""


class Color(StrEnum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


CubesSet = dict[Color, int]


@dataclass(frozen=True, slots=True)
class Game:
    id: int
    sets: list[CubesSet]

    def minimum_power(self) -> int:
        minimum_cubes = {color: 0 for color in Color}
        for cubes_set in self.sets:
            for color, count in cubes_set.items():
                prev_count = minimum_cubes[color]
                minimum_cubes[color] = max(prev_count, count)
        return self.power(minimum_cubes)

    @staticmethod
    def power(cubes_set: CubesSet) -> int:
        result = 1
        for _, value in cubes_set.items():
            result *= value
        return result

    @classmethod
    def from_line_to_parse(cls, line: str):
        game_id, cube_sets = line.split(":")
        id = get_int_from_str(game_id)
        sets = cls._parse_sets(cube_sets)
        return cls(id, sets)

    @staticmethod
    def _parse_sets(cube_sets: str):
        sets: list[CubesSet] = []
        for cube_set in cube_sets.split(";"):
            cubes: CubesSet = {}
            cubes_info = (cube.split() for cube in cube_set.split(","))
            for count, color in cubes_info:
                cubes[Color(color)] = int(count)
            sets.append(cubes)
        return sets

    def __iter__(self):
        for cubes_set in self.sets:
            yield cubes_set


@dataclass(frozen=True)
class GameValidator:
    max_number_cubes: CubesSet

    def is_valid(self, game: Game) -> bool:
        for cubes_set in game:
            for key, val in self.max_number_cubes.items():
                if cubes_set.get(key, 0) > val:
                    return False
        return True


def get_int_from_str(string: str):
    return int(re.search(r"\d+", string).group(0))  # type: ignore


def read_lines_from_file(path: str):
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            yield line


def games_id_sum(input):
    """Part 1"""
    validator = GameValidator(
        {
            Color.RED: 12,
            Color.GREEN: 13,
            Color.BLUE: 14,
        }
    )
    games = (Game.from_line_to_parse(line) for line in input)
    ids_sum = sum(game.id for game in games if validator.is_valid(game))
    print(ids_sum)


def power_set_cubes(input):
    """Part 2"""
    games = (Game.from_line_to_parse(line) for line in input)
    powers_sum = sum(game.minimum_power() for game in games)
    print(powers_sum)


def main():
    if len(sys.argv) < 2:
        input = (line for line in TEST_INPUT.splitlines())
    else:
        input = read_lines_from_file(sys.argv[1])
    # games_id_sum(input)
    power_set_cubes(input)


if __name__ == "__main__":
    main()
