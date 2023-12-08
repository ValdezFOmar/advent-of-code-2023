import re
import shutil
from pathlib import Path


def create_challenge():
    for file in Path.cwd().glob("day*.py"):
        dest_dir = Path.cwd() / "aoc" / file.stem
        dest_dir.mkdir()
        with open(dest_dir / "__init__.py", "w"):
            pass
        shutil.copyfile(src=file, dst=dest_dir / "challenge.py")


def move_input():
    for input_file in Path.cwd().glob("input*.txt"):
        print(input_file, str(input_file))
        match = re.search(r"\d+", str(input_file.name))
        if match is None:
            continue
        num_challenge = int(match.group(0))
        dest_dir = Path.cwd() / "aoc" / f"day{num_challenge}"
        dest_file = dest_dir / "input.txt"
        shutil.move(input_file, dest_file)


def create_file(path) -> None:
    with open(path, "w"):
        pass


def main():
    for dir in (Path.cwd() / "aoc").iterdir():
        create_file(dir / "__main__.py")
        create_file(dir / "test.py")


if __name__ == "__main__":
    main()
