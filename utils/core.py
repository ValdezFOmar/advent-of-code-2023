from typing import (Generic, Iterable, Iterator, MutableSet, NamedTuple,
                    Sequence, TypeVar)

T = TypeVar("T")
Matrix2D = Sequence[Sequence[T]]
Positions = MutableSet[tuple[int, int]]


class Cell(NamedTuple, Generic[T]):
    """Simple container for cells in a 2d array."""

    value: T
    row: int
    column: int


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
