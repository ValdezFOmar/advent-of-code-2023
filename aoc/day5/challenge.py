import re
from dataclasses import InitVar, dataclass, field
from itertools import chain
from typing import Iterable, Iterator

import utils.iterutils as itu
from aoc.tools import YieldStr, run_challenge


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
        upper_bound = (
            self.dest.stop if _range.stop == self.source.stop else self.map(_range.stop)
        )
        return range(self.map(_range.start), upper_bound)


@dataclass(slots=True)
class CategoryMapper:
    name: str
    iterable: InitVar[Iterable[MappingRange]]
    mapping_ranges: tuple[MappingRange, ...] = field(init=False)

    def __post_init__(self, iterable: Iterable[MappingRange]) -> None:
        if not iterable:
            raise ValueError("parameter 'iterable' can't be empty")
        self.mapping_ranges = tuple(sorted(iterable, key=self._sort_range_key))

    @staticmethod
    def _sort_range_key(mr: MappingRange):
        return mr.source.start, mr.source.stop

    def map(self, val: int) -> int:
        for mrange in self.mapping_ranges:
            if val in mrange.source:
                return mrange.map(val)
        return val

    def imap_range(self, r: range) -> Iterator[range]:
        # This method relias in mapping_ranges being sorted
        last_upper_bound = self.mapping_ranges[-1].source.stop
        original_r = r
        last_yielded = r
        for mrange in self.mapping_ranges:
            if r.stop <= mrange.source.start or r.start >= last_upper_bound:
                yield (last_yielded := r)
                break
            if r.start >= mrange.source.start and r.stop <= mrange.source.stop:
                if r:
                    yield (last_yielded := mrange.map_range(r))
                break
            lower_bound = itu.get_index(r, mrange.source.start)
            upper_bound = itu.get_index(r, mrange.source.stop)
            if lower_bound is not None:
                yield (last_yielded := r[:lower_bound])
            if None not in (lower_bound, upper_bound):
                contained_range = r[lower_bound:upper_bound]
                yield (last_yielded := mrange.map_range(contained_range))
            if upper_bound is not None and lower_bound is None:
                yield (last_yielded := r[:upper_bound])
            r = r[upper_bound:]
        if last_yielded != r and r != original_r:
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

    for category in categories:
        mapped_ranges = [category.map_range(seed_range) for seed_range in seeds_ranges]
        seeds_ranges = chain.from_iterable(mapped_ranges)
    return min(sr.start for sr in seeds_ranges)


if __name__ == "__main__":
    run_challenge(solution_part_2, __file__, debug=True)
