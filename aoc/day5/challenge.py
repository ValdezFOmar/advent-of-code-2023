import re
from dataclasses import InitVar, dataclass, field
from itertools import chain
from typing import Iterable, Iterator, NamedTuple

import utils.iterutils as itu
from aoc.tools import YieldStr, run_challenge


class RangeIntersections(NamedTuple):
    left: range | None
    middle: range | None
    right: range | None


@dataclass(slots=True)
class MappingRange:
    dest_start: int = field(repr=False)
    src_start: int = field(repr=False)
    length: int = field(repr=False)
    source: range = field(init=False)
    dest: range = field(init=False)

    def __post_init__(self) -> None:
        self.source = itu.length_range(self.src_start, self.length)
        self.dest = itu.length_range(self.dest_start, self.length)

    def map(self, val: int) -> int:
        if val not in self.source:
            raise ValueError(f"Cannot map value, '{val}' is out of {self.source}")
        i = self.source.index(val)
        return self.dest[i]

    def map_range(self, _range: range) -> range:
        if _range == self.source:
            return self.dest
        lower_bound = (
            self.map(_range.start)
            if _range.start != self.source.start
            else self.dest.start
        )
        upper_bound = (
            self.map(_range.stop) if _range.stop != self.source.stop else self.dest.stop
        )
        return range(lower_bound, upper_bound)

    def is_before(self, r: range) -> bool:
        return self.source.stop <= r.start

    def is_after(self, r: range) -> bool:
        return r.stop <= self.source.start

    def divide_by_intersections(self, r: range) -> RangeIntersections:
        if r in self:
            return RangeIntersections(None, r, None)

        lower_i = itu.get_index(r, self.source.start)
        upper_i = itu.get_index(r, self.source.stop)

        left = r[:lower_i] if lower_i not in {None, 0} else None
        right = r[upper_i:] if upper_i not in {None, 0} else None

        if left and right:
            middle = r[lower_i:upper_i]
        elif left and not right:
            middle = r[lower_i:]
        elif right and not left:
            middle = r[:upper_i]
        else:
            middle = None
        return RangeIntersections(left, middle, right)

    def __contains__(self, value) -> bool:
        if not isinstance(value, range):
            return False
        return value.start >= self.source.start and value.stop <= self.source.stop

    def __lt__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return (
            self.source.start,
            self.source.stop,
        ) < (
            other.source.start,
            other.source.stop,
        )


@dataclass
class CategoryMapper:
    name: str
    iterable: InitVar[Iterable[MappingRange]]
    mapping_ranges: tuple[MappingRange, ...] = field(init=False)

    def __post_init__(self, iterable: Iterable[MappingRange]) -> None:
        if not iterable:
            raise ValueError("parameter 'iterable' can't be empty")
        self.mapping_ranges = tuple(sorted(iterable))

    def map(self, val: int) -> int:
        for mrange in self.mapping_ranges:
            if val in mrange.source:
                return mrange.map(val)
        return val

    def imap_range(self, r: range) -> Iterator[range]:
        # This method relias in mapping_ranges being sorted
        first_range = self.mapping_ranges[0]
        last_range = self.mapping_ranges[-1]

        if first_range.is_after(r) or last_range.is_before(r):
            yield r
            return
        for mrange in self.mapping_ranges:
            if mrange.is_before(r):
                continue
            if r in mrange:
                yield mrange.map_range(r)
                return
            if mrange.is_after(r):
                yield r
                return
            intersections = mrange.divide_by_intersections(r)
            if intersections.left is not None:
                yield intersections.left
            if intersections.middle is not None:
                yield mrange.map_range(intersections.middle)
            if intersections.right is None:
                break
            r = intersections.right
        # if a right intersection happens at the last range, it might not be yield
        if r is not None and last_range.is_before(r):
            yield r

    def map_range(self, r: range) -> tuple[range, ...]:
        return tuple(self.imap_range(r))


def parse_input(input: YieldStr) -> tuple[list[int], Iterator[CategoryMapper]]:
    def parse_categories() -> Iterator[CategoryMapper]:
        mapping_ranges: list[MappingRange] = []
        capturing_category: bool = False
        name = ""

        group = "category"
        category_name = re.compile(rf"(?P<{group}>(\w|-)+)\s+map:")

        for line in input:
            if not capturing_category:
                if match := category_name.match(line):
                    capturing_category = True
                    name = match.group(group)
                continue

            if not line.strip() and capturing_category:
                yield CategoryMapper(name, mapping_ranges)
                capturing_category = False
                mapping_ranges = []
                name = ""
                continue

            range_marker = [int(num) for num in itu.find_numbers(line)]
            mapping_ranges.append(MappingRange(*range_marker))
        if mapping_ranges:
            yield CategoryMapper(name, mapping_ranges)

    seeds = [int(seed) for seed in itu.find_numbers(next(input))]
    return seeds, parse_categories()


def solution_part_1(input: YieldStr) -> int:
    seeds, categories = parse_input(input)
    for categorie in categories:
        seeds = map(categorie.map, seeds)
    return min(seeds)


def solution_part_2(input: YieldStr) -> int:
    seeds, categories = parse_input(input)
    seeds_ranges = [itu.length_range(*seed_pair) for seed_pair in itu.batched(seeds, 2)]

    for categorie in categories:
        mapped_seeds = [categorie.map_range(sr) for sr in seeds_ranges]
        seeds_ranges = chain.from_iterable(mapped_seeds)

    return min(sr.start for sr in seeds_ranges)


if __name__ == "__main__":
    run_challenge(solution_part_2, __file__, debug=True)
