from __future__ import annotations

import enum
import sys
from dataclasses import dataclass, field
from itertools import islice
from typing import ClassVar, Iterator, NamedTuple, TypeAlias

import utils.iterutils as itu
from aoc.tools import YieldStr, run_challenge

TilesGrid: TypeAlias = list[str]


class Point(NamedTuple):
    row: int
    column: int

    def __add__(self, other: object) -> Point:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.__class__(self.row + other.row, self.column + other.column)

    def __radd__(self, other: object) -> Point:
        return self.__add__(other)

    def __mul__(self, value: object) -> Point:
        if isinstance(value, int):
            return self.__class__(self.row * value, self.column * value)
        return NotImplemented


class Direction(Point, enum.Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    @property
    def opposite(self) -> Direction:
        return self.__class__(self.value * -1)  # pyright: ignore


@dataclass(slots=True, eq=False)
class Pipe:
    PIPE_TYPES: ClassVar[dict[str, frozenset[Direction]]] = {
        "|": frozenset({Direction.UP, Direction.DOWN}),
        "-": frozenset({Direction.LEFT, Direction.RIGHT}),
        "J": frozenset({Direction.UP, Direction.LEFT}),
        "L": frozenset({Direction.UP, Direction.RIGHT}),
        "7": frozenset({Direction.DOWN, Direction.LEFT}),
        "F": frozenset({Direction.DOWN, Direction.RIGHT}),
        "S": frozenset(),
    }

    pipe_type: str
    position: Point
    connections: frozenset[Direction] = field(init=False)

    def __post_init__(self) -> None:
        self.connections = self.PIPE_TYPES[self.pipe_type]

    def opposite_end(self, direction: Direction) -> Direction:
        [end] = {direction} ^ self.connections
        return end

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.pipe_type, self.position) == (other.pipe_type, other.position)
        return False


def parse_input(input: YieldStr) -> tuple[TilesGrid, Point]:
    tile_grid: TilesGrid = []
    s_tile = None

    for row, line in enumerate(input):
        if (column := itu.get_index(line, "S")) is not None:
            s_tile = Point(row, column)
        tile_grid.append(line)
    assert s_tile is not None
    return tile_grid, s_tile


def find_first_connection(grid: TilesGrid, point: Point) -> tuple[Pipe, Direction]:
    for direction in Direction:
        offset = point + direction
        tile = grid[offset.row][offset.column]
        if tile not in Pipe.PIPE_TYPES:
            continue
        pipe = Pipe(tile, offset)
        if direction.opposite in pipe.connections:
            return pipe, direction
    raise RuntimeError("Connected pipe not found")


def find_pipes_loop(tile_grid: TilesGrid, start: Point) -> Iterator[Pipe]:
    pipe, direction = find_first_connection(tile_grid, start)
    starting_pipe = Pipe("S", start)
    starting_pipe.connections |= {direction}

    yield starting_pipe

    while True:
        yield pipe
        direction = pipe.opposite_end(direction.opposite)
        position = pipe.position + direction
        row, col = position
        pipe = Pipe(tile_grid[row][col], position)
        if pipe == starting_pipe:
            starting_pipe.connections |= {direction.opposite}
            break


def solution_part_1(input: YieldStr) -> int:
    tile_grid, starting_point = parse_input(input)
    pipes = find_pipes_loop(tile_grid, starting_point)
    steps_to_farthest_pipe = itu.ilen(pipes) // 2
    return steps_to_farthest_pipe


def solution_part_2(input: YieldStr) -> int:
    tile_grid, starting_point = parse_input(input)
    pipes_loop = set[Point]()

    top_most_row = sys.maxsize
    bottom_most_row = 0
    left_most_column = sys.maxsize
    right_most_column = 0

    for pipe in find_pipes_loop(tile_grid, starting_point):
        pipes_loop.add(pipe.position)
        top_most_row = min(top_most_row, pipe.position.row)
        bottom_most_row = max(bottom_most_row, pipe.position.row)
        left_most_column = min(left_most_column, pipe.position.column)
        right_most_column = max(right_most_column, pipe.position.column)

    print(
        f"{top_most_row=}",
        f"{bottom_most_row=}",
        f"{left_most_column=}",
        f"{right_most_column=}",
        sep="\n",
    )

    for row, line in enumerate(islice(tile_grid, top_most_row, bottom_most_row), top_most_row):
        pass

    return 0


if __name__ == "__main__":
    run_challenge(solution_part_2, __file__, debug=True)
