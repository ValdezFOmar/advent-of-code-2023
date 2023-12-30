from __future__ import annotations

import functools
from pathlib import Path
from typing import TYPE_CHECKING, Callable, Iterator, TypeAlias

if TYPE_CHECKING:
    from _typeshed import StrPath


YieldStr: TypeAlias = Iterator[str]


def read_lines_from_file(path: StrPath) -> Iterator[str]:
    """Yields one line at a time for a given file."""
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            yield line.strip()


def relative_input_file_path(relative_to: str, name: str | None = None) -> str:
    """Finds and retrieves the path of a *input.txt file."""
    if name is None:
        name = "test-input.txt"
    path = Path(relative_to)
    path = path.parent / name if not path.is_dir() else path / name
    return str(path)


def relative_test_file(
    relative_to: str,
    name: str | None = None,
    reader: Callable[[StrPath], Iterator[str]] | None = None,
) -> Iterator[str]:
    """Automatically creates a generator for test-input.txt file."""
    path = relative_input_file_path(relative_to, name)
    reader = reader or read_lines_from_file
    return reader(path)


def format_output(solution_name: str, output: int) -> str:
    return f"{solution_name}: {output:<15,}{output}"


def run_challenge(
    solution: Callable[[Iterator[str]], int],
    relative_to: str,
    reader: Callable[[StrPath], Iterator[str]] | None = None,
    *,
    debug: bool = False,
) -> None:
    """Runs the challenge solution with the given input and prints its output."""
    name = None if debug else "input.txt"
    output = solution(relative_test_file(relative_to, name, reader))
    real_func = solution.func if isinstance(solution, functools.partial) else solution
    print(format_output(real_func.__name__, output))


def run_challenge_with_path(
    solution: Callable[[str], int],
    relative_to: str,
    *,
    debug: bool = False,
) -> None:
    """Like `run_challenge` but retrieves the file path of the input file instead of a iterator."""
    name = None if debug else "input.txt"
    output = solution(relative_input_file_path(relative_to, name))
    print(format_output(solution.__name__, output))
