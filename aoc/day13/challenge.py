import itertools as itt
from pprint import pprint
from typing import Iterator, TypeAlias

from aoc.tools import YieldStr, run_challenge
from utils import matrix

Note: TypeAlias = list[str]

HORIZONTAL_FACTOR = 100
VERTICAL_FACTOR = 1


def retrieve_notes(input: YieldStr) -> Iterator[Note]:
    capturing_note = False
    note: Note = []

    for line in input:
        if not line:
            if capturing_note:
                yield note
                note = []
                capturing_note = False
            continue
        if not capturing_note:
            capturing_note = True
        note.append(line)
    # There migth not be a empty line at the end
    if capturing_note:
        yield note


def is_perfect_reflection(note: matrix.Matrix2D[object], index: int) -> bool:
    up_ptr = index
    down_ptr = index + 1
    while up_ptr >= 0 and down_ptr < len(note):
        if note[up_ptr] != note[down_ptr]:
            return False
        up_ptr -= 1
        down_ptr += 1
    return True


def reflection_line(note: matrix.Matrix2D[object]) -> int | None:
    """Find the line of reflection for a perfect reflexion."""
    for line, (row, next_row) in enumerate(itt.pairwise(note)):
        if row != next_row:
            continue
        if is_perfect_reflection(note, line):
            return line
    return None


def solution_part_1(input: YieldStr) -> int:
    notes_sum = 0
    for note in retrieve_notes(input):
        line_factor = HORIZONTAL_FACTOR
        if (line := reflection_line(note)) is None:
            line = reflection_line(matrix.transpose(note))
            line_factor = VERTICAL_FACTOR
        assert line is not None
        line += 1  # Compensate for index starting at 0
        notes_sum += line * line_factor
    return notes_sum


def solution_part_2(input: YieldStr) -> int:
    return 0


if __name__ == "__main__":
    run_challenge(solution_part_1, __file__, debug=True)
