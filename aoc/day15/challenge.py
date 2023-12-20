from typing import Iterator

from aoc.tools import YieldStr, run_challenge


def read_until_comma(path) -> Iterator[str]:
    text = ""
    with open(path, "r", encoding="utf-8") as file:
        while char := file.read(1):
            if char == "\n":
                continue
            if char == ",":
                if text:
                    yield text
                    text = ""
                continue
            text += char
        if text:
            yield text


def hash_string(string: str) -> int:
    result = 0
    for char in string:
        result += ord(char)
        result *= 17
        result %= 256
    return result


def solution_part_1(input: YieldStr) -> int:
    return sum(hash_string(step) for step in input)


def solution_part_2(input: YieldStr) -> int:
    return 0


if __name__ == "__main__":
    run_challenge(solution_part_1, __file__, read_until_comma, debug=True)
