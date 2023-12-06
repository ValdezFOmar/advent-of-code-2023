import sys
from typing import Generator

YieldStr = Generator[str, None, None]


def read_lines_from_file(path):
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            yield line


TEST_INPUT = """\
"""


def part_1(input: YieldStr, testing: bool):
    TEST_OUTPUT = 0

    output = 0
    print(output)

    if testing:
        assert output == TEST_OUTPUT


def part_2(input: YieldStr, testing: bool):
    TEST_OUTPUT = 0

    output = 0

    if testing:
        assert output == TEST_OUTPUT


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
