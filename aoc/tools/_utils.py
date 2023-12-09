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
            yield line


def run_challenge(
    solution: Callable[[Iterator[str]], object],
    input_challenge: Iterator[str] | None = None,
    /,
    relative_to: StrPath | None = None,
    debug: bool = False,
) -> None:
    """Runs the challenge solution with the given input and prints its output."""
    if input_challenge is not None:
        output = solution(input_challenge)
    elif relative_to is not None:
        defualt_input = "input.txt" if not debug else "test-input.txt"
        path = Path(relative_to)
        path = (
            path.parent / defualt_input if not path.is_dir() else path / defualt_input
        )
        input = read_lines_from_file(path)
        output = solution(input)
    else:
        raise TypeError(f"You must provide either 'input_challenge' or 'relative_to'")

    print(f"{solution.__name__}: {output}")
