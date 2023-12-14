"""Utilities for iterating and working with iterables / sequences."""


import re
from functools import reduce
from itertools import islice
from typing import Iterable, Iterator, Sequence, TypeVar

T = TypeVar("T")

_nums_regex = re.compile(r"-?\d+")
iter_numbers = _nums_regex.finditer
find_numbers = _nums_regex.findall


def get_index(seq: Sequence[T], value: T) -> int | None:
    try:
        return seq.index(value)
    except ValueError:
        return None


def length_range(start: int, length: int) -> range:
    return range(start, start + length)


# Taken from https://docs.python.org/3.12/library/itertools.html#itertools.batched
# This function is only available in ^3.12
def batched(iterable: Iterable[T], n: int) -> Iterator[tuple[T, ...]]:
    """batched('ABCDEFG', 3) --> ABC DEF G"""
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch


def items_difference(sequence: Sequence[int]) -> Iterator[list[int]]:
    if isinstance(sequence, list):
        yield sequence
    else:
        yield list(sequence)

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
