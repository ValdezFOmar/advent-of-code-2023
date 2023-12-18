import math
import re
from itertools import cycle
from typing import Callable, Iterator, NamedTuple

from aoc.tools import YieldStr, run_challenge


class Node(NamedTuple):
    left: str
    right: str


Network = dict[str, Node]


def parse_input(input: YieldStr) -> tuple[str, Network]:
    instructions = next(input).strip()
    node_expression = re.compile(r"^(?P<node>\w+)\s*=\s*\((?P<left>\w+),\s*(?P<right>\w+)\)$")
    network: Network = {}
    for line in input:
        match = node_expression.match(line)
        if match is None:
            continue
        node = match.group("node")
        left = match.group("left")
        right = match.group("right")
        network[node] = Node(left, right)
    return instructions, network


def walk_network(start: str, directions: str, network: Network) -> Iterator[str]:
    current_node = network[start]
    next_node = start
    for direction in cycle(directions):
        yield next_node
        if direction == "L":
            next_node = current_node.left
        elif direction == "R":
            next_node = current_node.right
        current_node = network[next_node]


def steps_until_condition(
    start: str,
    end_condition: Callable[[str], bool],
    directions: str,
    network: Network,
) -> int:
    steps = 0
    for node in walk_network(start, directions, network):
        if end_condition(node):
            break
        steps += 1
    return steps


def steps_to_node(start: str, target: str, directions: str, network: Network) -> int:
    return steps_until_condition(start, lambda node: node == target, directions, network)


def solution_part_1(input: YieldStr) -> int:
    directions, network = parse_input(input)
    steps = steps_to_node("AAA", "ZZZ", directions, network)
    return steps


# Get how many steps would take for every node to get to
# its first node ending with 'Z', then get the LCM
def solution_part_2(input: YieldStr) -> int:
    directions, network = parse_input(input)
    starting_nodes = [node for node in network if node.endswith("A")]
    steps_to_end_nodes = [
        steps_until_condition(node, lambda n: n.endswith("Z"), directions, network)
        for node in starting_nodes
    ]
    steps = math.lcm(*steps_to_end_nodes)
    return steps


if __name__ == "__main__":
    run_challenge(solution_part_1, relative_to=__file__, debug=True)
