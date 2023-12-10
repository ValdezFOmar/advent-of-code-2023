import re
from itertools import islice
from typing import Iterator, Sequence

_nums_regex = re.compile(r"-?\d+")
iter_numbers = _nums_regex.finditer
find_numbers = _nums_regex.findall


def items_difference(sequence: Sequence[int]) -> Iterator[Sequence[int]]:
    yield sequence

    while True:
        sequence = [
            item - prev_item
            for prev_item, item in zip(sequence, islice(sequence, 1, None))
        ]
        yield sequence


def predict_next_number(sequence: Sequence[int]) -> int | None:
    """Returns the predicted numbers, return `None` if it can't be predicted."""
    last_items: list[int] = []
    for next_sequence in items_difference(sequence):
        if not next_sequence:
            break
        last_items.append(next_sequence[-1])
        if not any(next_sequence):
            break
    return sum(last_items)
