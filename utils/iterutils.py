"""Utilities for iterating and working with iterables / sequences."""

import enum
import itertools
import operator
import re
from functools import reduce
from typing import Iterable, Iterator, Sequence, TypeVar

T = TypeVar("T")

_nums_regex = re.compile(r"-?\d+")
iter_numbers = _nums_regex.finditer
find_numbers = _nums_regex.findall


class _Empty(enum.Enum):
    TOKEN = 0


_empty = _Empty.TOKEN


def mul(iterable: Iterable[int]) -> int:
    """Like `sum()` but multiply instead of adding."""
    return reduce(operator.mul, iterable)


def last_item(iterator: Iterator[T]) -> T:
    """Exhausts an iterator and return the last item."""
    item: T | _Empty = _empty
    for item in iterator:
        pass
    if item is _empty:
        raise ValueError("Iterator is empty")
    return item


def divide_by(value: object, iterable: Iterable[T]) -> Iterator[tuple[T, ...]]:
    """Divide iterable into subsequences at the given value."""
    values: list[T] = []

    for item in iterable:
        if item != value:
            values.append(item)
        else:
            yield tuple(values)
            values = []
    yield tuple(values)


def join_from_iter(iterable: Iterable[Iterable[T]], value: T) -> Iterator[T]:
    """Like str.join(), but yield the elements of the iterables inside another iterable."""
    iters = iter(iterable)
    try:
        first_it = next(iters)
    except StopIteration:
        return
    yield from first_it
    for it in iters:
        yield value
        for item in it:
            yield item


def get_index(seq: Sequence[object], value: object) -> int | None:
    try:
        return seq.index(value)
    except ValueError:
        return None


def length_range(start: int, length: int) -> range:
    return range(start, start + length)


def ilen(iterable: Iterable[object]) -> int:
    """len(), but for iterators/generators."""
    return reduce(lambda l, _: l + 1, iterable, 0)


# Taken from https://docs.python.org/3.12/library/itertools.html#itertools.batched
# This function is only available in ^3.12
def batched(iterable: Iterable[T], n: int) -> Iterator[tuple[T, ...]]:
    """Batch data into tuples of length n. The last batch may be shorter.

    batched('ABCDEFG', 3) --> ABC DEF G
    """
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(itertools.islice(it, n)):
        yield batch


# https://docs.python.org/3.11/library/itertools.html#itertools-recipes
def ncycles(iterable: Iterator[T], n: int) -> Iterator[T]:
    """Returns the sequence elements n times"""
    return itertools.chain.from_iterable(itertools.repeat(tuple(iterable), n))


def items_difference(sequence: Sequence[int]) -> Iterator[list[int]]:
    if isinstance(sequence, list):
        yield sequence
    else:
        yield list(sequence)

    while True:
        sequence = [
            item - prev_item
            for prev_item, item in zip(sequence, itertools.islice(sequence, 1, None))
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
