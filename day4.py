import re
import sys
from dataclasses import dataclass
from typing import Generator

YieldStr = Generator[str, None, None]


@dataclass
class Card:
    winning_numbers: frozenset[int]
    card_numbers: frozenset[int]

    @property
    def points(self) -> int:
        win_nums_that_appear = len(self.winning_numbers & self.card_numbers)
        multiplier = win_nums_that_appear - 1
        return 2 ** (multiplier) if win_nums_that_appear != 0 else 0

    @classmethod
    def from_line(cls, line: str):
        numbers = line.split(":")[-1]
        winning_numbers, card_numbers = numbers.split("|")
        winning_numbers = cls._extract_numbers(winning_numbers)
        card_numbers = cls._extract_numbers(card_numbers)
        return cls(winning_numbers, card_numbers)

    @staticmethod
    def _extract_numbers(string: str):
        return frozenset(int(num) for num in re.findall(r"\d+", string))


def read_lines_from_file(path):
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            yield line


TEST_INPUT = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""


def part_1(input: YieldStr, testing: bool):
    TEST_OUTPUT = 13

    cards = (Card.from_line(line) for line in input)
    card_points = sum(card.points for card in cards)
    print(card_points)

    if testing:
        assert card_points == TEST_OUTPUT


def part_2(input: YieldStr):
    pass


def main():
    testing = False
    if len(sys.argv) < 2:
        input = (line for line in TEST_INPUT.splitlines())
        testing = True
    else:
        input = read_lines_from_file(sys.argv[1])
    part_1(input, testing)


if __name__ == "__main__":
    main()
