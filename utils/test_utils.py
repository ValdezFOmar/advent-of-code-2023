import pytest

from .iterutils import predict_prev_number
from .matrix import adjacent_cells_to_cell, adjacent_cells_to_line, calc_position_deviation

# fmt: off
MATRIX = [
    # 0   1   2   3   4
    [ 1,  2,  3,  4,  5],  # 0
    [ 6,  7,  8,  9, 10],  # 1
    [11, 12, 13, 14, 15],  # 2
    [16, 17, 18, 19, 20],  # 3
    [21, 22, 23, 24, 25],  # 4
]
LENGTH_ROWS = len(MATRIX)
LENGTH_COLS = len(MATRIX[0])

@pytest.mark.parametrize("matrix, pos, cells", [
    (MATRIX, (2, 2), [7, 8, 9, 12, 14, 17, 18, 19]),
    (MATRIX, (0, 0), [2, 6, 7]),
    (MATRIX, (3, 4), [14, 15, 19, 24, 25]),
])
def test_adjacent_to_cell(matrix, pos, cells):
    cells_value = [cell.value for cell in adjacent_cells_to_cell(matrix, *pos)]
    assert cells_value == cells


@pytest.mark.parametrize("matrix, pos, cells", [
    (MATRIX, (4, 0, 3), [16, 17, 18, 19, 24]),
    (MATRIX, (1, 2, 4), [2, 3, 4, 5, 7, 10, 12, 13, 14, 15]),
    (MATRIX, (3, 1, 5), [11, 12, 13, 14, 15, 16, 21, 22, 23, 24, 25]),
])
def test_adjacent_to_line(matrix, pos, cells):
    cells_value = [cell.value for cell in adjacent_cells_to_line(matrix, *pos)]
    assert cells_value == cells


@pytest.mark.parametrize("position, deviation", [
    ((2, LENGTH_ROWS, 2, 3, LENGTH_COLS), (-1, 2, -1, 2)),
    ((4, LENGTH_ROWS, 0, 3, LENGTH_COLS), (-1, 1,  0, 4)),
    ((1, LENGTH_ROWS, 2, 4, LENGTH_COLS), (-1, 2, -1, 3)),
    ((3, LENGTH_ROWS, 1, 5, LENGTH_COLS), (-1, 2, -1, 4)),
    ((0, LENGTH_ROWS, 3, 5, LENGTH_COLS), ( 0, 2, -1, 2)),
])
def test_deviation(position, deviation):
    assert calc_position_deviation(*position) == deviation


@pytest.mark.parametrize("seq, prev_num", [
    ((0, 3, 6, 9, 12, 15,),   -3),
    ((1, 3, 6, 10, 15, 21,),   0),
    ((10, 13, 16, 21, 30, 45,),5),
])
def test_prev_number(seq, prev_num):
    assert predict_prev_number(seq) == prev_num
