import enum
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import TypeAlias

from aoc.tools import YieldStr, run_challenge
from utils.matrix import Direction
from utils.matrix import Vector as Point

Map: TypeAlias = list[str]


@dataclass(slots=True)
class HikePath:
    path: set[Point]
    current_position: Point
    previous_position: Point

    def __len__(self) -> int:
        return len(self.path)

    def add_position(self, position: Point) -> None:
        self.path.add(position)
        self.previous_position = self.current_position
        self.current_position = position

    def output_hike(self, layout_map: Map, file_name: str | None = None) -> None:
        file_name = file_name or "output.txt"
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)

        new_map = [list(row) for row in layout_map]
        for point in self.path:
            row, column = point
            new_map[row][column] = "O"

        with open(output_dir / file_name, "w", encoding="utf-8") as output:
            for row in new_map:
                print("".join(row), file=output)


class Tile(enum.StrEnum):
    PATH = "."
    FOREST = "#"
    UP_SLOPE = "^"
    DOWN_SLOPE = "v"
    LEFT_SLOPE = "<"
    RIGHT_SLOPE = ">"

    # pylint: disable=R0916
    def can_pass(self, direction: Direction) -> bool:
        if self is Tile.FOREST:
            return False
        if (
            (self is Tile.PATH)
            or (self is Tile.UP_SLOPE and direction is Direction.UP)
            or (self is Tile.DOWN_SLOPE and direction is Direction.DOWN)
            or (self is Tile.LEFT_SLOPE and direction is Direction.LEFT)
            or (self is Tile.RIGHT_SLOPE and direction is Direction.RIGHT)
        ):
            return True
        return False


def allowed_paths(layout_map: Map, position: Point, previous_position: Point | None) -> list[Point]:
    row_limits = range(len(layout_map))
    column_limits = range(len(layout_map[0]))
    directions = list(Direction)

    if previous_position is not None:
        directions.remove(Direction(previous_position - position))  # pyright: ignore

    paths: list[Point] = []
    for direction in directions:
        path = position + direction
        if not (path.row in row_limits and path.column in column_limits):
            continue
        tile = Tile(layout_map[path.row][path.column])
        if not tile.can_pass(direction):
            continue
        paths.append(path)
    return paths


def find_paths(layout_map: Map, start: Point, end: Point) -> list[HikePath]:
    final_paths: list[HikePath] = []
    queue = deque([HikePath(set(), start, start + Direction.UP)])

    while queue:
        path = queue.popleft()
        while path.current_position != end:
            positions = allowed_paths(layout_map, path.current_position, path.previous_position)
            next_position = positions.pop(0)
            if positions:
                for position in positions:
                    new_path = path.path.copy()
                    new_path.add(position)
                    queue.append(HikePath(new_path, position, path.current_position))
            path.add_position(next_position)
        final_paths.append(path)
    return final_paths


def dump_paths(layout: Map, hike_paths: list[HikePath]) -> None:
    for i, hike_path in enumerate(hike_paths, 1):
        hike_path.output_hike(layout, f"output-{i:0>3}.txt")


def solution_part_1(input: YieldStr) -> int:
    island_map = list(input)
    start_column = island_map[0].index(Tile.PATH)
    end_column = island_map[-1].index(Tile.PATH)

    start_position = Point(0, start_column)
    end_position = Point(len(island_map) - 1, end_column)

    hike_paths = find_paths(island_map, start_position, end_position)
    # dump_paths(island_map, hike_paths)

    return max(len(hike_path) for hike_path in hike_paths)


def solution_part_2(input: YieldStr) -> int:
    return 0


if __name__ == "__main__":
    run_challenge(solution_part_1, __file__, debug=True)
