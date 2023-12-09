from typing import Generic, NamedTuple, Sequence, TypeVar

T = TypeVar("T")
Matrix2D = Sequence[Sequence[T]]


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


def adjacent_cells_to_line(  # pylint: disable=too-many-locals
    matrix: Matrix2D[T],
    pos_row: int,
    pos_column_start: int,
    pos_column_end: int,
) -> tuple[Cell[T], ...]:
    """
    Returns the cells around the area defined by the position parameters.
    Parameter `pos_column_end` is exclusive.
    """
    max_row, max_column = len(matrix), len(matrix[0])
    start_row, end_row, start_column, end_column = calc_position_deviation(
        pos_row, max_row, pos_column_start, pos_column_end, max_column
    )

    adjancent_cells: list[Cell[T]] = []

    for row_deviation in range(start_row, end_row):
        for column_deviation in range(start_column, end_column):
            if (
                row_deviation == 0
                and pos_column_start
                <= column_deviation + pos_column_start
                <= pos_column_end - 1
            ):
                continue

            current_row = pos_row + row_deviation
            current_column = pos_column_start + column_deviation
            cell_value = matrix[current_row][current_column]

            adjancent_cells.append(Cell(cell_value, current_row, current_column))

    return tuple(adjancent_cells)


def adjacent_cells_to_cell(
    matrix: Matrix2D[T], row: int, col: int
) -> tuple[Cell[T], ...]:
    """Adjacent cells to a single cell."""
    return adjacent_cells_to_line(matrix, row, col, col + 1)
