"""Utilities for iterating and working with iterables / sequences."""


import re
from functools import reduce
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


def predict_next_number(sequence: Sequence[int]) -> int:
    """Returns the predicted number."""
    last_items: list[int] = []
    for next_sequence in items_difference(sequence):
        if not next_sequence:
            break
        last_items.append(next_sequence[-1])
        if not any(next_sequence):
            break
    return sum(last_items)


def predict_prev_number(sequence: Sequence[int]) -> int:
    """Returns the previous predicted number of the sequence."""
    first_items: list[int] = []
    for next_sequence in items_difference(sequence):
        if not next_sequence:
            break
        # Insert in reverse order so reduce operates from the buttom up
        first_items.insert(0, next_sequence[0])
        if not any(next_sequence):
            break
    return reduce(lambda acc, n: n - acc, first_items)
