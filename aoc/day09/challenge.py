from aoc.tools import YieldStr, run_challenge
from utils.iterutils import find_numbers, predict_next_number, predict_prev_number


def retrive_sequences(input: YieldStr):
    for line in input:
        yield [int(num) for num in find_numbers(line)]


def solution_part_1(input: YieldStr) -> int:
    output = 0
    for sequence in retrive_sequences(input):
        output += predict_next_number(sequence)
    return output


def solution_part_2(input: YieldStr) -> int:
    return sum(predict_prev_number(sequence) for sequence in retrive_sequences(input))


if __name__ == "__main__":
    run_challenge(solution_part_1, __file__)
