from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Callable, Iterator

if TYPE_CHECKING:
    from _typeshed import StrPath


YieldStr = Iterator[str]


def read_lines_from_file(path: StrPath) -> Iterator[str]:
    """Yields one line at a time for a given file."""
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            yield line.strip()


def relative_test_file(relative_to: StrPath, name: str | None = None) -> Iterator[str]:
    """Automatically creates a generator for test-input.txt file."""
    if name is None:
        name = "test-input.txt"
    path = Path(relative_to)
    path = path.parent / name if not path.is_dir() else path / name
    return read_lines_from_file(path)


def run_challenge(
    solution: Callable[[Iterator[str]], object],
    relative_to: StrPath,
    *,
    debug: bool = False,
) -> None:
    """Runs the challenge solution with the given input and prints its output."""
    name = None if debug else "input.txt"
    output = solution(relative_test_file(relative_to, name))
    print(f"{solution.__name__}: {output:<20,}{output}")
