import itertools
import re
import sys
from typing import Generator, Generic, NamedTuple, Sequence, TypeVar

T = TypeVar("T")

TEST_INPUT = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""
TEST_RESULT = 4361


VALID_SYMBOLS = frozenset({"@", "%", "-", "/", "*", "#", "=", "$", "+", "&"})


class Cell(NamedTuple, Generic[T]):
    value: T
    row: int
    column: int


def read_lines_from_file(path):
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            yield line


def get_adjacent_values(
    matrix: Sequence[Sequence[T]],
    pos_row: int,
    pos_column_start: int,
    pos_column_end: int,
) -> list[Cell[T]]:
    max_row, max_column = len(matrix), len(matrix[0])

    adjancent_cells: list[Cell[T]] = []

    start_row = -1 if pos_row > 0 else 0
    end_row = 2 if pos_row < max_row - 1 else 1
    start_column = -1 if pos_column_start > 0 else 0
    end_column = (
        (pos_column_end - pos_column_start) + 1
        if pos_column_end < max_column - 1
        else 1
    )

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

    return adjancent_cells


def part_1(input: Generator[str, None, None]):
    first_line = next(input)
    only_dots = "." * len(first_line)
    queue: list[str] = [only_dots, only_dots, first_line]
    middle_line = 1

    sum_numbers = 0

    for line in itertools.chain(input, [only_dots]):
        queue.pop(0)
        queue.append(line)
        for number in re.finditer(r"\d+", queue[middle_line]):
            cells = get_adjacent_values(
                queue,
                middle_line,
                number.start(),
                number.end(),
            )
            symbols = {cell.value for cell in cells}
            if not symbols & VALID_SYMBOLS:
                continue

            sum_numbers += int(number.group(0))

    # assert sum_numbers == TEST_RESULT
    print(sum_numbers)


# i dont know, got stuck
def part_2(input: Generator[str, None, None]):
    first_line = next(input)
    only_dots = "." * len(first_line)
    queue: list[str] = [only_dots, only_dots, first_line]
    middle_line = 1

    sum_gear_ratios = 0

    for line in itertools.chain(input, [only_dots]):
        queue.pop(0)
        queue.append(line)
        for gear in re.finditer(r"\*", queue[middle_line]):
            cells = get_adjacent_values(
                queue,
                middle_line,
                gear.start(),
                gear.end(),
            )
            print(gear.span())
            symbols = {cell.value for cell in cells}
            if not symbols & VALID_SYMBOLS:
                continue
        # sum_gear_ratios += int(number.group(0))

    # assert sum_numbers == TEST_RESULT
    print(sum_gear_ratios)


def main():
    if len(sys.argv) < 2:
        input = (line for line in TEST_INPUT.splitlines())
    else:
        input = read_lines_from_file(sys.argv[1])
    part_2(input)


if __name__ == "__main__":
    main()
