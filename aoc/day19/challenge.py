import operator
import re
from dataclasses import InitVar, dataclass, field
from itertools import takewhile
from typing import Callable, Iterable, Iterator, TypeAlias

from aoc.tools import YieldStr, run_challenge
from utils.iterutils import last_item

Part: TypeAlias = dict[str, int]


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

    def __str__(self) -> str:
        return f"{self.category}{self.op_str}{self.value}:{self.destination}"


# Parts can contain more than one Rule for any part category and the order matters.
# Rules are stored in list for this reason, instead of a dictionary.
@dataclass(slots=True)
class Workflow:
    name: str
    rules: list[Rule]
    default_dest: str

    _workflow_regex = re.compile(r"(?P<name>\w+){(?P<rules>.+)}")

    def part_destination(self, part: Part) -> str:
        for rule in self.rules:
            value = part.get(rule.category)
            if value is None:
                continue
            if rule.valid(value):
                return rule.destination
        return self.default_dest

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

    def __str__(self) -> str:
        rules = ",".join(str(rule) for rule in self.rules)
        rules += f",{self.default_dest}"
        return f"{self.name}{{{rules}}}"


@dataclass
class PartValidator:
    workflows: InitVar[Iterable[Workflow]]
    _workflows: dict[str, Workflow] = field(init=False)

    ACCEPTED = "A"
    REJECTED = "R"

    def __post_init__(self, workflows: Iterable[Workflow]) -> None:
        self._workflows = {w.name: w for w in workflows}
        assert "in" in self._workflows

    def is_accepted(self, part: Part) -> bool:
        last_destination = last_item(self.destinations(part))
        return last_destination == self.ACCEPTED

    def destinations(self, part: Part) -> Iterator[str]:
        destination = "in"
        while True:
            yield destination
            if destination in (self.ACCEPTED, self.REJECTED):
                return
            workflow = self._workflows[destination]
            destination = workflow.part_destination(part)


def parse_part(string: str) -> Part:
    string = string.replace("{", "(").replace("}", ")")
    string = "dict" + string
    return eval(string)  # pylint: disable=W0123


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


def solution_part_2(input: YieldStr) -> int:
    return 0


if __name__ == "__main__":
    run_challenge(solution_part_1, __file__, debug=True)
