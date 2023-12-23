# pylint: disable=W0621
from itertools import takewhile

import pytest

from aoc.tools import relative_test_file

from .challenge import PartValidator, Rule, Workflow, solution_part_1, solution_part_2


@pytest.fixture
def part_validator():
    file_input = relative_test_file(__file__)
    workflows = (Workflow.from_line(line) for line in takewhile(bool, file_input))
    return PartValidator(workflows)


@pytest.mark.parametrize(
    "solution, output",
    [
        (solution_part_1, 19114),
        (solution_part_2, 0),
    ],
)
def test_solution(solution, output):
    assert solution(relative_test_file(__file__)) == output


@pytest.mark.parametrize(
    "workflow, parts",
    [
        (
            Workflow("AlwaysAccepts", {"x": Rule("<", 0, "None")}, "A"),
            [
                ({"x": 2655}, PartValidator.ACCEPTED),
                ({"s": 44}, PartValidator.ACCEPTED),
                ({"m": 264}, PartValidator.ACCEPTED),
                ({"s": 1339}, PartValidator.ACCEPTED),
                ({"m": 1623}, PartValidator.ACCEPTED),
                ({"a": 3000}, PartValidator.ACCEPTED),
            ],
        ),
    ],
)
def test_worlflow(workflow, parts):
    for part, destination in parts:
        assert workflow.destination(part) == destination


@pytest.mark.parametrize(
    "workflow, parts",
    [
        (
            Workflow(
                name="ShouldReject",
                rules={
                    "x": Rule(">", 1000, PartValidator.REJECTED),
                    "m": Rule(">", 0, PartValidator.ACCEPTED),
                },
                default_dest=PartValidator.ACCEPTED,
            ),
            [
                {"x": 7870, "m": 2655},
                {"x": 1679, "m": 4411},
                {"x": 2036, "m": 2649},
                {"x": 2461, "m": 1339},
                {"x": 2127, "m": 1623},
                {"x": 1500, "m": 3000},
            ],
        ),
    ],
)
def test_reject_parts(workflow, parts):
    for part in parts:
        assert workflow.destination(part) == PartValidator.REJECTED


@pytest.mark.parametrize(
    "part, xdestinations",
    [
        ({"x": 787, "m": 2655, "a": 1222, "s": 2876}, ("in", "qqz", "qs", "lnx", "A")),
        ({"x": 1679, "m": 44, "a": 2067, "s": 496}, ("in", "px", "rfg", "gd", "R")),
        ({"x": 2036, "m": 264, "a": 79, "s": 2244}, ("in", "qqz", "hdj", "pv", "A")),
        ({"x": 2461, "m": 1339, "a": 466, "s": 291}, ("in", "px", "qkq", "crn", "R")),
        ({"x": 2127, "m": 1623, "a": 2188, "s": 1013}, ("in", "px", "rfg", "A")),
        ({"s": 1000, "m": 3000}, ("in", "px", "A")),
        # ({}, ()),
    ],
)
def test_workflows_destinations(part_validator, part, xdestinations):
    destinations = part_validator.destinations(part)
    for dest, expected_dest in zip(destinations, xdestinations):
        assert dest == expected_dest
