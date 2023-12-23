from __future__ import annotations

import enum
import re
import sys
from abc import ABC, abstractmethod
from collections import deque
from dataclasses import InitVar, dataclass, field
from typing import ClassVar, Iterable, NamedTuple

from aoc.tools import YieldStr, run_challenge


class Bit(enum.IntEnum):
    OFF = 0
    ON = 1

    @classmethod
    def flip(cls, b: Bit) -> Bit:
        return cls((b + 1) & 1)


class Pulse(NamedTuple):
    bit: Bit
    sender: str
    destination: str

    def __repr__(self) -> str:
        return f"{self.sender} -{self.bit.name}-> {self.destination}"


@dataclass
class Module(ABC):
    name: str
    destination_modules: list[str]
    state: Bit = field(init=False, default=Bit.OFF)
    _last_pulse: Bit = field(init=False, default=Bit.OFF, repr=False)

    prefix: ClassVar[str] = ""

    def receive_pulse(self, pulse: Pulse) -> None:
        self._last_pulse = pulse.bit

    @abstractmethod
    def send_pulse(self) -> list[Pulse]:
        raise NotImplementedError

    def state_str(self) -> str:
        return f"{self.prefix}{self.name} is {self.state.name}"

    def __str__(self) -> str:
        modules = ", ".join(self.destination_modules)
        return f"{self.prefix}{self.name} -> {modules}"


class FlipFlop(Module):
    prefix = "%"

    def receive_pulse(self, pulse: Pulse) -> None:
        super().receive_pulse(pulse)
        if pulse.bit is Bit.ON:
            return
        self.state = Bit.flip(self.state)

    def send_pulse(self) -> list[Pulse]:
        if self._last_pulse is Bit.ON:
            return []
        return [Pulse(self.state, self.name, module) for module in self.destination_modules]


class Conjunction(Module):
    prefix = "&"

    def __init__(
        self,
        name: str,
        input_modules: Iterable[str],
        destination_modules: list[str],
    ):
        self._input_modules: dict[str, Bit] = {mod: Bit.OFF for mod in input_modules}
        super().__init__(name, destination_modules)

    def register_input(self, module: Module) -> None:
        self._input_modules[module.name] = Bit.OFF

    def receive_pulse(self, pulse: Pulse) -> None:
        super().receive_pulse(pulse)
        assert pulse.sender in self._input_modules
        self._input_modules[pulse.sender] = pulse.bit

    def send_pulse(self) -> list[Pulse]:
        bit_to_send = Bit.ON
        if all(self._input_modules.values()):
            bit_to_send = Bit.OFF
        return [Pulse(bit_to_send, self.name, mod) for mod in self.destination_modules]

    def state_str(self) -> str:
        inputs_state = ", ".join(
            f"'{mod}' as {state.name}" for mod, state in self._input_modules.items()
        )
        return f"{super().state_str()} with inputs {inputs_state}"

    def __str__(self) -> str:
        input_mods = ", ".join(self._input_modules)
        return f"{super().__str__()}\t<- {input_mods}"


class EndModule(Module):
    def __init__(self, name: str) -> None:
        super().__init__(name, [])

    def send_pulse(self) -> list[Pulse]:
        return []


class Broadcaster(Module):
    NAME = "broadcaster"

    def __init__(self, destination_modules: list[str] | None = None):
        if destination_modules is None:
            destination_modules = []
        super().__init__(self.NAME, destination_modules=destination_modules)

    def receive_pulse(self, pulse: Pulse) -> None:
        self.state = pulse.bit
        super().receive_pulse(pulse)

    def send_pulse(self) -> list[Pulse]:
        return [Pulse(self._last_pulse, self.name, module) for module in self.destination_modules]


@dataclass
class ModuleComunicator:
    modules: InitVar[Iterable[Module]]
    _modules: dict[str, Module] = field(init=False)
    pulses_queue: deque[Pulse] = field(init=False, default_factory=deque)
    total_high_pulses: int = field(init=False, default=0)
    total_low_pulses: int = field(init=False, default=0)

    def __post_init__(self, modules: Iterable[Module]) -> None:
        self._modules = {mod.name: mod for mod in modules}
        assert Broadcaster.NAME in self._modules
        self._register_conjunction_inputs()

    def _register_conjunction_inputs(self) -> None:
        end_modules: list[EndModule] = []
        for module in self._modules.values():
            for dest_module_name in module.destination_modules:
                dest_module = self._modules.get(dest_module_name)
                if dest_module is None:
                    print(
                        f"Module with name '{dest_module_name}'"
                        " doesn't exist, creating EndModule...",
                        file=sys.stderr,
                    )
                    end_modules.append(EndModule(dest_module_name))
                if not isinstance(dest_module, Conjunction):
                    continue
                dest_module.register_input(module)
        for end_module in end_modules:
            self._modules[end_module.name] = end_module

    def print_modules(self):
        for module in self._modules.values():
            print(module)

    def print_modules_state(self):
        for module in self._modules.values():
            print(module.state_str())

    def _count_pulse(self, pulse: Pulse):
        if pulse.bit is Bit.OFF:
            self.total_low_pulses += 1
        else:
            self.total_high_pulses += 1

    def push_button(self, n: int = 1):
        for _ in range(n):
            initial_pulse = Pulse(Bit.OFF, "button", Broadcaster.NAME)
            self.pulses_queue.append(initial_pulse)

            while self.pulses_queue:
                pulse = self.pulses_queue.popleft()
                self._count_pulse(pulse)
                dest_module = self._modules[pulse.destination]
                dest_module.receive_pulse(pulse)
                next_pulses = dest_module.send_pulse()
                self.pulses_queue.extend(next_pulses)


def parse_input(input: YieldStr) -> list[Module]:
    modules: list[Module] = []
    for line in input:
        module, destinations = re.split(r"\s*->\s*", line)
        destinations = re.split(r"\s*,\s*", destinations)
        if not re.match("[%&]", module):
            modules.append(Broadcaster(destinations))
            continue
        prefix = module[0]
        name = module[1:]
        if prefix == FlipFlop.prefix:
            modules.append(FlipFlop(name, destinations))
        elif prefix == Conjunction.prefix:
            modules.append(Conjunction(name, [], destinations))
    return modules


def solution_part_1(input: YieldStr) -> int:
    modules = parse_input(input)
    modcom = ModuleComunicator(modules)
    modcom.push_button(n=1000)
    return modcom.total_high_pulses * modcom.total_low_pulses


def solution_part_2(input: YieldStr) -> int:
    return 0


if __name__ == "__main__":
    run_challenge(solution_part_1, __file__, debug=True)
