import re
from pathlib import Path

single_digit_day = re.compile(r"^day(?P<num>\d)$")
aoc_dir = Path.cwd() / "aoc"

for directory in (d for d in aoc_dir.iterdir() if d.is_dir()):
    match = single_digit_day.match(directory.name)
    if not match:
        continue
    day = int(match.group("num"))
    left_padded = directory.with_name(f"day{day:0>2}")
    directory.rename(left_padded)
