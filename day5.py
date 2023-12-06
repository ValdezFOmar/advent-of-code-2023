import functools
import itertools
import re
import sys
from dataclasses import dataclass
from typing import Generator, Iterable, TypeVar

YieldStr = Generator[str, None, None]
T = TypeVar("T")

TEST_INPUT = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""


@dataclass(slots=True)
class RangeMapper:
    dest_start: int
    source_start: int
    lenght: int

    def map(self, value: int) -> int:
        offset = self.dest_start - self.source_start
        return value + offset

    def __contains__(self, item: int) -> bool:
        return item in range_by_length(self.source_start, self.lenght)


@dataclass
class Mapper:
    name: str
    mapping_ranges: list[RangeMapper]

    def map(self, value: int) -> int:
        for mapping_range in self.mapping_ranges:
            if value in mapping_range:
                return mapping_range.map(value)
        return value


class MappersParser:
    def __init__(self, text: YieldStr) -> None:
        seeds = next(text)
        self.seeds = [int(num) for num in re.findall(r"\d+", seeds)]
        self.mappers: list[Mapper] = []
        self._parse(text)

    def _parse(self, text: YieldStr):
        mapping_ranges: list[RangeMapper] = []
        capturing_mapper: bool = False

        mapper_re_group = "mapper"
        mapper_header = re.compile(rf"(?P<{mapper_re_group}>(\w|-)+)\s+map:")
        range_markers = re.compile(r"\d+")

        for line in text:
            if not capturing_mapper:
                matched_mapper = mapper_header.match(line)
                if matched_mapper:
                    capturing_mapper = True
                    mapper_name = matched_mapper.group(mapper_re_group)
                    self.mappers.append(Mapper(mapper_name, mapping_ranges))
                continue

            if not line.strip() and capturing_mapper:
                capturing_mapper = False
                mapping_ranges = []
                continue

            range_marker = [int(num) for num in range_markers.findall(line)]
            mapping_ranges.append(RangeMapper(*range_marker))


def read_lines_from_file(path):
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            yield line


# Taken from https://docs.python.org/3.12/library/itertools.html?highlight=itertools#itertools.batched
def batched(iterable: Iterable[T], n: int):
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(itertools.islice(it, n)):
        yield batch


@functools.cache
def range_by_length(start: int, lenght: int, step: int = 1) -> range:
    """range_by_length(2, 5) --> 2 3 4 5 6"""
    return range(start, start + lenght, step)


def part_1(input: YieldStr, testing: bool):
    TEST_OUTPUT = 35

    parsed_input = MappersParser(input)
    seeds, mappers = parsed_input.seeds, parsed_input.mappers

    for mapper in mappers:
        seeds = [mapper.map(seed) for seed in seeds]

    output = min(seeds)
    print(output)

    if testing:
        assert output == TEST_OUTPUT


# Really slow, better run it with pypy
def part_2(input: YieldStr, testing: bool):
    TEST_OUTPUT = 46

    parsed_input = MappersParser(input)
    mappers = parsed_input.mappers
    seeds = (
        range_by_length(start, length)
        for start, length in batched(parsed_input.seeds, 2)
    )

    lowest_location = sys.maxsize

    for seed in itertools.chain.from_iterable(seeds):
        mapped_seed = seed
        for mapper in mappers:
            mapped_seed = mapper.map(mapped_seed)
        lowest_location = min(mapped_seed, lowest_location)

    print(lowest_location)

    if testing:
        assert lowest_location == TEST_OUTPUT


def main():
    testing = False
    if len(sys.argv) < 2:
        input = (line for line in TEST_INPUT.splitlines())
        testing = True
    else:
        input = read_lines_from_file(sys.argv[1])
    part_2(input, testing)


if __name__ == "__main__":
    main()
