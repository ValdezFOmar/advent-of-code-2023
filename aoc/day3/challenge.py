import itertools
import re

from aoc.tools import YieldStr, run_challenge
from utils import adjacent_cells_to_cell, adjacent_cells_to_line

VALID_SYMBOLS = frozenset({"@", "%", "-", "/", "*", "#", "=", "$", "+", "&"})


def solution_part_1(input: YieldStr) -> int:
    first_line = next(input)
    only_dots = "." * len(first_line)
    queue: list[str] = [only_dots, only_dots, first_line]
    middle_line = 1

    sum_numbers = 0

    for line in itertools.chain(input, [only_dots]):
        queue.pop(0)
        queue.append(line)
        for number in re.finditer(r"\d+", queue[middle_line]):
            cells = adjacent_cells_to_line(
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
    return 0


def solution_part_2(input: YieldStr) -> int:
    first_line = next(input)
    only_dots = "." * len(first_line)
    queue: list[str] = [only_dots, only_dots, first_line]
    middle_line = 1
    sum_gear_ratios = 0

    for line in itertools.chain(input, [only_dots]):
        queue.pop(0)
        queue.append(line)
        for gear in re.finditer(r"\*", queue[middle_line]):
            cells = adjacent_cells_to_cell(
                queue,
                middle_line,
                gear.start(),
            )
            print(gear.span())
            symbols = {cell.value for cell in cells}
            if not symbols & VALID_SYMBOLS:
                continue
        # sum_gear_ratios += int(number.group(0))

    # assert sum_numbers == TEST_RESULT
    print(sum_gear_ratios)
    return 0


if __name__ == "__main__":
    run_challenge(solution_part_2, __file__, debug=True)
