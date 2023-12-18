import pytest

from aoc.tools import relative_test_file

from .challenge import CategoryMapper, MappingRange, solution_part_1, solution_part_2


@pytest.mark.parametrize(
    "solution, output",
    [
        (solution_part_1, 35),
        (solution_part_2, 46),
    ],
)
def test_solution(solution, output):
    assert solution(relative_test_file(__file__)) == output


@pytest.mark.parametrize(
    "range_, mapped_range",
    [
        (range(7, 10), range(52, 55)),
        (range(10, 10), range(55, 55)),
        (range(5, 15), range(50, 60)),
        (range(15, 25), range(60, 70)),
        (range(6, 24), range(51, 69)),
        (range(5, 25), range(50, 70)),
    ],
)
def test_map_range_to_range(range_, mapped_range):
    mrange = MappingRange(50, 5, 20)
    assert mrange.map_range(range_) == mapped_range


@pytest.mark.parametrize(
    "range_",
    [
        range(50, 70),
        range(25, 29),
        range(30, 40),
        range(26, 29),
    ],
)
def test_before(range_):
    mrange = MappingRange(50, 5, 20)
    assert mrange.is_before(range_)


@pytest.mark.parametrize("range_", [range(2), range(1), range(4), range(5)])
def test_after(range_):
    mrange = MappingRange(50, 5, 20)
    assert mrange.is_after(range_)


@pytest.mark.parametrize(
    "val, mapped_val",
    [
        (5, 50),
        (9, 54),
        (15, 60),
        (20, 65),
        (24, 69),
    ],
)
def map_single_value(val, mapped_val):
    mrange = MappingRange(50, 5, 20)
    assert mrange.map(val) == mapped_val


@pytest.mark.parametrize(
    "range_, intersections",
    [
        (range(4), (None, None, None)),
        (range(20), (None, None, None)),
        (range(67, 100), (None, None, None)),
        (range(50, 100), (None, None, None)),
        (range(20, 50), (None, range(20, 50), None)),
        (range(25, 45), (None, range(25, 45), None)),
        (range(20, 25), (None, range(20, 25), None)),
        (range(30, 50), (None, range(30, 50), None)),
        (range(35, 60), (None, range(35, 50), range(50, 60))),
        (range(20, 60), (None, range(20, 50), range(50, 60))),
        (range(35), (range(20), range(20, 35), None)),
        (range(50), (range(20), range(20, 50), None)),
        (range(70), (range(20), range(20, 50), range(50, 70))),
    ],
)
def test_intersections(range_, intersections):
    mrange = MappingRange(0, 20, 30)  # source = range(20, 50)
    assert mrange.divide_by_intersections(range_) == intersections


# fmt: off
@pytest.mark.parametrize(
    "range_, xresult",
    [
        [range(20),      (range(20),)],
        [range(100, 101),(range(100, 101),)],
        [range(50),      (range(45), range(81, 86))],
        [range(70, 110), (range(74, 81), range(45, 68), range(100, 110))],
        [range(99, 101), (range(67, 68), range(100, 101))],
        [range(60, 80),  (range(96, 100),range(68, 81), range(45, 48))],
    ],
)
def test_category_mapper(range_, xresult):
    category = CategoryMapper(
        "test",
        [
            MappingRange(45, 77, 23),  # [77,100)
            MappingRange(81, 45, 19),  # [45,64)
            MappingRange(68, 64, 13),  # [64,77)
        ],
    )
    assert category.map_range(range_) == xresult
