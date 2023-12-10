from aoc.tools import YieldStr, run_challenge
from utils.iterutils import find_numbers, predict_next_number


def retrive_sequences(input: YieldStr):
    for line in input:
        yield [int(num) for num in find_numbers(line)]


def solution_part_1(input: YieldStr) -> int:
    output = 0
    p = __file__.removesuffix("challenge.py")
    with open(p + "output.txt", "w", encoding="utf-8") as file:
        for i, sequence in enumerate(retrive_sequences(input), 1):
            num = predict_next_number(sequence)
            if num is not None:
                output += num
            print(i, num, file=file)
    return output


def solution_part_2(input: YieldStr) -> int:
    return 0


if __name__ == "__main__":
    run_challenge(solution_part_1, __file__)
