import re
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
    boxes: list[dict[str, int]] = [{} for _ in range(256)]
    sign = re.compile(r"[-=]")

    for step in input:
        label, num = sign.split(step)
        match = sign.search(step)
        assert match is not None

        operation_char = match.group(0)
        label_hash = hash_string(label)

        if operation_char == "=":
            boxes[label_hash][label] = int(num)
        elif operation_char == "-":
            box = boxes[label_hash]
            if label in box:
                del box[label]

    total_focusing_power = 0

    for box_num, box in enumerate(boxes, 1):
        for slot, focal_length in enumerate(box.values(), 1):
            total_focusing_power += box_num * slot * focal_length

    return total_focusing_power


if __name__ == "__main__":
    run_challenge(solution_part_2, __file__, read_until_comma, debug=True)
