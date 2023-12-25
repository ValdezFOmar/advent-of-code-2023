from __future__ import annotations

import enum
import operator
from typing import Generic, Iterable, Iterator, MutableSet, NamedTuple, Sequence, TypeAlias, TypeVar

T = TypeVar("T")
Matrix2D: TypeAlias = Sequence[Sequence[T]]  # pylint: disable=C0103
Positions: TypeAlias = MutableSet[tuple[int, int]]


class Vector(NamedTuple):
    """Simple class for making operations with vectors."""

    row: int
    column: int

    def __str__(self) -> str:
        return f"({self.row}, {self.column})"

    def manhattan_distance(self, point: Vector, /) -> int:
        return self.horizontal_distance(point) + self.vertical_distance(point)

    def horizontal_distance(self, point: Vector, /) -> int:
        return abs(self.row - point.row)

    def vertical_distance(self, point: Vector, /) -> int:
        return abs(self.column - point.column)

    def _operation(self, other: object, operation) -> Vector:
        if isinstance(other, type(self)):
            return self.__class__(
                operation(self.row, other.row), operation(self.column, other.column)
            )
        if isinstance(other, int):
            return self.__class__(operation(self.row, other), operation(self.column, other))
        return NotImplemented

    def __add__(self, other: object) -> Vector:
        return self._operation(other, operator.add)

    def __iadd__(self, other: object) -> Vector:
        return self.__add__(other)

    def __radd__(self, other: object) -> Vector:
        return self.__add__(other)

    def __sub__(self, other: object) -> Vector:
        return self._operation(other, operator.sub)

    def __mul__(self, value: object) -> Vector:
        return self._operation(value, operator.mul)


class Direction(Vector, enum.Enum):
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)

    @property
    def opposite(self) -> Direction:
        return self.__class__(self.value * -1)  # pyright: ignore


class Cell(NamedTuple, Generic[T]):
    """Simple container for cells in a 2d array."""

    value: T
    row: int
    column: int


def itranspose(m: Iterable[Iterable[T]], /) -> Iterator[tuple[T, ...]]:
    """Same as `transpose`, but in iterator form."""
    return zip(*m, strict=True)


def transpose(m: Matrix2D[T], /) -> list[tuple[T, ...]]:
    """Transpose a matrix, turning columns into rows and rows into columns."""
    return list(itranspose(m))


def calc_position_deviation(
    pos_row: int,
    max_row: int,
    pos_column_start: int,
    pos_column_end: int,
    max_column: int,
) -> tuple[int, int, int, int]:
    """Returns (start_row, end_row, start_column, end_column)"""
    start_row = -1 if pos_row > 0 else 0
    end_row = 2 if pos_row < max_row - 1 else 1
    start_column = -1 if pos_column_start > 0 else 0
    end_column = (
        (pos_column_end - pos_column_start) + 1
        if pos_column_end < max_column - 1
        else max_column - pos_column_start
    )
    return start_row, end_row, start_column, end_column


def adjacent_cells(
    matrix: Matrix2D[T],
    pos_row: int,
    pos_column_start: int,
    pos_column_end: int,
) -> Iterator[Cell[T]]:
    """
    Iterates over the cells around the area defined by the position parameters.
    Parameter `pos_column_end` is exclusive.
    """
    max_row, max_column = len(matrix), len(matrix[0])
    start_row, end_row, start_column, end_column = calc_position_deviation(
        pos_row, max_row, pos_column_start, pos_column_end, max_column
    )

    for row_deviation in range(start_row, end_row):
        for column_deviation in range(start_column, end_column):
            if (
                row_deviation == 0
                and pos_column_start <= column_deviation + pos_column_start <= pos_column_end - 1
            ):
                continue

            current_row = pos_row + row_deviation
            current_column = pos_column_start + column_deviation
            cell_value = matrix[current_row][current_column]

            yield Cell(cell_value, current_row, current_column)


def adjacent_cells_to_line(
    matrix: Matrix2D[T],
    pos_row: int,
    pos_column_start: int,
    pos_column_end: int,
) -> Iterator[Cell[T]]:
    """
    Returns the cells around the area defined by the position parameters.
    Parameter `pos_column_end` is exclusive.
    """
    return adjacent_cells(matrix, pos_row, pos_column_start, pos_column_end)


def adjacent_cells_to_cell(matrix: Matrix2D[T], row: int, col: int) -> Iterator[Cell[T]]:
    """Adjacent cells to a single cell."""
    return adjacent_cells(matrix, row, col, col + 1)


def inline_number_from_cell(
    matrix: Matrix2D[str],
    cell: Cell[str],
    visited_positions: Positions,
) -> str:
    number = cell.value
    left_ptr = -1
    right_ptr = 1
    left_stop = False
    right_stop = False

    while not (left_stop and right_stop):
        left_deviation = cell.column + left_ptr
        right_deviation = cell.column + right_ptr
        left_value = matrix[cell.row][left_deviation]
        right_value = matrix[cell.row][right_deviation]

        if left_value.isdigit():
            visited_positions.add((cell.row, left_deviation))
            number = left_value + number
            left_ptr += -1
        else:
            left_stop = True

        if right_value.isdigit():
            visited_positions.add((cell.row, right_deviation))
            number = number + right_value
            right_ptr += 1
        else:
            right_stop = True

    return number


def find_adjacent_numbers(
    matrix: Matrix2D[str],
    row: int,
    col: int,
    *,
    cells: Iterable[Cell[str]] | None = None,
) -> Iterator[int]:
    """Return the all the adjacent numbers to a single cell."""
    if cells is None:
        cells = adjacent_cells_to_cell(matrix, row, col)
    visited_positions: Positions = set()

    for cell in cells:
        if (cell.row, cell.column) in visited_positions:
            continue
        if not cell.value.isdigit():
            continue
        number = inline_number_from_cell(matrix, cell, visited_positions)
        yield int(number)
