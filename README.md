# Advent of Code 2023

My solutions to [Advent of Code 2023](https://adventofcode.com/2023).


## Installation

You will need `poetry` installed on your system. Run:

```sh
python -m venv .venv
source .venv/bin/activate
poetry install
```


## Testing

To run all test:

```sh
pytest
```

Run tests for a specific day challenge with:

```sh
pytest aoc/day[n]/
```

Where `n` is a number for a specific day.

For linting use:
```sh
pylint .
```
