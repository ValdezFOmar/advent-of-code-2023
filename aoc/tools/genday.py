"""Script for generating a subpackage for a 'Advent of Code' day challenge."""


import argparse
import shutil
import sys
from pathlib import Path


def error_msg(msg: str) -> int:
    script_name = Path(sys.argv[0]).name
    print(f"{script_name}: {msg}")
    return 1


def main() -> int | str:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "day", metavar="D", help="The day to use for naming the subpakage.", type=int
    )
    args = parser.parse_args()

    project_root = Path(__file__).parent.parent
    template_dir = Path(__file__).parent / "_day_template"

    if not (template_dir.exists() and template_dir.is_dir()):
        return error_msg("Couldn't find template directory")

    dest_path = project_root / f"day{args.day}"

    if dest_path.exists():
        return error_msg("The subpackage for this day already exits.")

    dest_copied = shutil.copytree(src=template_dir, dst=dest_path)
    print("Subpacke create at:", dest_copied)

    return 0


if __name__ == "__main__":
    sys.exit(main())
