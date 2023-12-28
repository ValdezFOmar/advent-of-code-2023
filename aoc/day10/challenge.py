from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar, Iterator, TypeAlias

import utils.iterutils as itu
from aoc.tools import YieldStr, run_challenge
from utils import extra_math
from utils.matrix import Direction, Point

TilesGrid: TypeAlias = list[str]


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
    points = [pipe.position for pipe in find_pipes_loop(tile_grid, starting_point)]
    area = extra_math.shoelace_formula(points)
    return extra_math.number_interior_points(area, len(points))


if __name__ == "__main__":
    run_challenge(solution_part_1, __file__, debug=True)
