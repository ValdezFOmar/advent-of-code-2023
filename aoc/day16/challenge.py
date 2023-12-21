from __future__ import annotations

import io
from dataclasses import dataclass, field
from functools import reduce
from typing import Sequence

from aoc.tools import YieldStr, run_challenge
from utils.matrix import Direction, Vector


class Tile:
    __slots__ = "_char", "hit_directions", "_is_energized"

    EMPTY = "."
    _tile_types = {}

    def __init_subclass__(cls, chars: str, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        for char in chars:
            cls._tile_types[char] = cls

    def __new__(cls, char: str):
        if len(char) != 1:
            raise ValueError("char must be a 1 character string")
        subclass = cls._tile_types.get(char, Tile)
        return object.__new__(subclass)

    def __init__(self, char: str, /) -> None:
        if char not in self._tile_types:
            char = self.EMPTY
        self._char = char
        self.hit_directions = set()
        self._is_energized = False

    @property
    def is_energized(self):
        return self._is_energized

    def energized(self):
        self._is_energized = True
        self._char = "#"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self._char)})"

    def __str__(self) -> str:
        return self._char


class Mirror(Tile, chars="/\\"):
    __slots__ = ("_map_directions",)

    _mirror_types = {
        "/": {
            Direction.UP: Direction.RIGHT,
            Direction.DOWN: Direction.LEFT,
            Direction.LEFT: Direction.DOWN,
            Direction.RIGHT: Direction.UP,
        },
        "\\": {
            Direction.UP: Direction.LEFT,
            Direction.DOWN: Direction.RIGHT,
            Direction.LEFT: Direction.UP,
            Direction.RIGHT: Direction.DOWN,
        },
    }

    def __init__(self, char) -> None:
        self._map_directions = self._mirror_types[char]
        super().__init__(char)

    def reflect(self, beam: Beam) -> None:
        beam.direction = self._map_directions[beam.direction]


class Splitter(Tile, chars="|-"):
    __slots__ = ("_split_directions",)

    _splitter_types = {
        "|": ({Direction.RIGHT, Direction.LEFT}, (Direction.UP, Direction.DOWN)),
        "-": ({Direction.UP, Direction.DOWN}, (Direction.RIGHT, Direction.LEFT)),
    }

    def __init__(self, char) -> None:
        self._split_directions = self._splitter_types[char]
        super().__init__(char)

    def split(self, beam: Beam) -> Beam | None:
        directions = None
        if beam.direction in self._split_directions[0]:
            directions = self._split_directions[1]
        if directions is None:
            return None
        dir1, dir2 = directions
        beam.direction = dir1
        return Beam(beam.position, dir2)


@dataclass(slots=True)
class Beam:
    position: Vector
    direction: Direction
    active: bool = field(init=False, default=True)

    def hit_tile(self, tile: Tile) -> None:
        if self.direction in tile.hit_directions:
            self.active = False
            return
        tile.energized()
        tile.hit_directions.add(self.direction)

    def __hash__(self) -> int:
        return id(self)

    def update(self) -> None:
        self.position += self.direction

    def within_range(self, rows: range, columns: range) -> bool:
        return self.position.row in rows and self.position.column in columns


@dataclass(slots=True)
class Contraption:
    layout: Sequence[Sequence[Tile]]
    beams: set[Beam] = field(init=False, default_factory=set)

    def __post_init__(self):
        self.beams.add(Beam(Vector(0, -1), Direction.RIGHT))

    @classmethod
    def from_input(cls, input: YieldStr):
        contraption: list[list[Tile]] = []
        for line in input:
            contraption.append([Tile(char) for char in line])
        return cls(contraption)

    def init_simulation(self):
        rows = range(0, len(self.layout))
        columns = range(0, len(self.layout[0]))

        while self.beams:
            beams_to_add = set()
            beams_to_remove = set()

            for beam in self.beams:
                beam.update()

                if not beam.within_range(rows, columns):
                    beams_to_remove.add(beam)
                    continue

                tile = self[beam.position]
                beam.hit_tile(tile)

                if not beam.active:
                    beams_to_remove.add(beam)
                    continue

                if isinstance(tile, Mirror):
                    tile.reflect(beam)
                elif isinstance(tile, Splitter):
                    if (new_beam := tile.split(beam)) is not None:
                        beams_to_add.add(new_beam)

            self.beams.update(beams_to_add)
            self.beams.difference_update(beams_to_remove)

    def count_energized_tiles(self) -> int:
        def sum_row(acc: int, tile: Tile) -> int:
            if tile.is_energized:
                return acc + 1
            return acc

        return sum(reduce(sum_row, row, 0) for row in self.layout)

    def __str__(self) -> str:
        buf = io.StringIO()
        for row in self.layout:
            str_row = "".join(str(tile) for tile in row)
            print(str_row, file=buf)
        return buf.getvalue()

    def __getitem__(self, key: object) -> Tile:
        if isinstance(key, Vector):
            return self.layout[key.row][key.column]
        return NotImplemented


def solution_part_1(input: YieldStr) -> int:
    contraption = Contraption.from_input(input)
    contraption.init_simulation()
    count = contraption.count_energized_tiles()
    return count


def solution_part_2(input: YieldStr) -> int:
    return 0


if __name__ == "__main__":
    run_challenge(solution_part_1, __file__, debug=True)
