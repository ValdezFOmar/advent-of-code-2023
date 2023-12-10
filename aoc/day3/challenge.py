import itertools
import re

from aoc.tools import YieldStr, run_challenge
from utils import adjacent_cells_to_line, find_adjacent_numbers

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
    return sum_numbers


def solution_part_2(input: YieldStr) -> int:
    first_line = next(input)
    only_dots = "." * len(first_line)
    queue: list[str] = [only_dots, only_dots, first_line]
    middle_line = 1
    sum_gear_ratios = 0
    gear_pattern = re.compile(r"\*")

    for line in itertools.chain(input, [only_dots]):
        queue.pop(0)
        queue.append(line)
        for gear in gear_pattern.finditer(queue[middle_line]):
            numbers = list(find_adjacent_numbers(queue, middle_line, gear.start()))
            if len(numbers) != 2:
                continue
            sum_gear_ratios += numbers[0] * numbers[1]

    return sum_gear_ratios


if __name__ == "__main__":
    run_challenge(solution_part_2, __file__, debug=True)
