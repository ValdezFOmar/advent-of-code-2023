""" Beaten B) """


import sys

import regex as re

# Expected answer = 281
TEST_INPUT = """\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""

SPELLED_NUMBERS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}
NUMBERS_REGEX = "|".join((*SPELLED_NUMBERS, r"\d"))


def write_output(number_pairs):
    with open("output.txt", "w", encoding="utf-8") as file:
        for number_pair in number_pairs:
            print(number_pair, file=file)


def read_lines_from_file(path):
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            yield line


def convert_to_number_repr(str_num):
    if num := SPELLED_NUMBERS.get(str_num):
        return num
    return str_num


# Version 2, including spelled numbers
def find_first_and_last_numbers(line, regex):
    all_matches = re.findall(regex, line, overlapped=True)
    first = convert_to_number_repr(all_matches[0])
    last = convert_to_number_repr(all_matches[-1])
    return first, last


def main():
    if len(sys.argv) < 2:
        input = (line for line in TEST_INPUT.splitlines())
    else:
        input = read_lines_from_file(sys.argv[1])

    number_pairs = (find_first_and_last_numbers(line, NUMBERS_REGEX) for line in input)
    count = sum(int(first + last) for first, last in number_pairs)
    print(count)


if __name__ == "__main__":
    main()
