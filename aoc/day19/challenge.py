import operator
import re
from collections import deque
from dataclasses import dataclass, field
from itertools import takewhile
from typing import Callable, Iterable, Iterator, TypeAlias

from aoc.tools import YieldStr, run_challenge
from utils.iterutils import get_index, last_item, mul

Part: TypeAlias = dict[str, int]
PartRange: TypeAlias = dict[str, range]


@dataclass(slots=True)
class Rule:
    category: str
    op_str: str
    value: int
    destination: str
    operation: Callable[[int, int], bool] = field(init=False)

    _rules_types = {">": operator.gt, "<": operator.lt}

    def __post_init__(self) -> None:
        self.operation = self._rules_types[self.op_str]

    def valid(self, value: int) -> bool:
        return self.operation(value, self.value)

    def split_part_range(self, part: PartRange):
        values_range = part[self.category]
        index = get_index(values_range, self.value)

        if self.op_str == "<":
            if index is not None:
                match = replace_category(part, self.category, values_range[:index])
                no_match = replace_category(part, self.category, values_range[index:])
                return match, no_match
            if values_range.stop <= self.value:
                match = replace_category(part, self.category, values_range)
                return match, None
        else:  # self.op_str == '>'
            if index is not None:
                match = replace_category(part, self.category, values_range[index + 1 :])
                no_match = replace_category(part, self.category, values_range[: index + 1])
                return match, no_match
            if values_range.start > self.value:
                match = replace_category(part, self.category, values_range)
                return match, None

        # if no condition applied, then the range is just returned unchanged
        return None, part

    def __str__(self) -> str:
        return f"{self.category}{self.op_str}{self.value}:{self.destination}"


# Workflows can contain more than one Rule for any part category, and the order matters.
# Rules are stored in a list for this reason, instead of a dictionary.
@dataclass(slots=True, frozen=True)
class Workflow:
    name: str
    rules: list[Rule]
    default_dest: str

    _workflow_regex = re.compile(r"(?P<name>\w+){(?P<rules>.+)}")

    @classmethod
    def from_line(cls, line: str):
        match = cls._workflow_regex.match(line)
        assert match is not None
        raw_rules = match.group("rules").split(",")
        defualt_rule = raw_rules.pop()

        rules: list[Rule] = []
        for rule in raw_rules:
            cond, dest = rule.split(":")
            category = cond[0]
            operation = cond[1]
            value = int(cond[2:])
            rules.append(Rule(category, operation, value, dest))

        name = match.group("name")
        return cls(name, rules, defualt_rule)

    def part_destination(self, part: Part) -> str:
        for rule in self.rules:
            value = part.get(rule.category)
            if value is None:
                continue
            if rule.valid(value):
                return rule.destination
        return self.default_dest

    def part_range_destinations(self, part_range: PartRange) -> list[tuple[PartRange, str]]:
        part_with_destination: list[tuple[PartRange, str]] = []
        current_part = part_range

        for rule in self.rules:
            match, no_match = rule.split_part_range(current_part)
            if match is not None:
                part_with_destination.append((match, rule.destination))
            if no_match is not None:
                current_part = no_match
            else:
                return part_with_destination

        part_with_destination.append((current_part, self.default_dest))
        return part_with_destination

    def __str__(self) -> str:
        rules = ",".join(str(rule) for rule in self.rules)
        rules += f",{self.default_dest}"
        return f"{self.name}{{{rules}}}"


class PartValidator:
    ACCEPTED = "A"
    REJECTED = "R"

    def __init__(self, workflows: Iterable[Workflow]) -> None:
        self.workflows = {w.name: w for w in workflows}
        assert "in" in self.workflows

    def is_accepted(self, part: Part) -> bool:
        last_destination = last_item(self.destinations(part))
        return last_destination == self.ACCEPTED

    def destinations(self, part: Part) -> Iterator[str]:
        destination = "in"
        while True:
            yield destination
            if destination in (self.ACCEPTED, self.REJECTED):
                return
            workflow = self.workflows[destination]
            destination = workflow.part_destination(part)


def parse_part(string: str) -> Part:
    string = string.replace("{", "(").replace("}", ")")
    string = "dict" + string
    return eval(string)  # pylint: disable=W0123


def replace_category(part: PartRange, category: str, r: range) -> PartRange:
    copy = part.copy()
    copy[category] = r
    return copy


def solution_part_1(input: YieldStr) -> int:
    workflows = (Workflow.from_line(line) for line in takewhile(bool, input))
    pv = PartValidator(workflows)
    total = 0

    for line in input:
        part = parse_part(line)
        if not pv.is_accepted(part):
            continue
        total += sum(part.values())

    return total


# Think of parts as sets
def solution_part_2(input: YieldStr) -> int:
    parts_to_evaluate: deque[tuple[PartRange, str]]

    workflows = (Workflow.from_line(line) for line in takewhile(bool, input))
    workflows = {w.name: w for w in workflows}

    all_possible_parts = {char: range(1, 4001) for char in "xmas"}
    parts_to_evaluate = deque([(all_possible_parts, "in")])
    accepted_parts: list[PartRange] = []

    while parts_to_evaluate:
        part, destination = parts_to_evaluate.popleft()

        if destination == PartValidator.ACCEPTED:
            accepted_parts.append(part)
            continue
        if destination == PartValidator.REJECTED:
            continue

        workflow = workflows[destination]
        parts_to_evaluate.extend(workflow.part_range_destinations(part))

    return sum(mul(map(len, part.values())) for part in accepted_parts)


if __name__ == "__main__":
    run_challenge(solution_part_2, __file__, debug=True)
