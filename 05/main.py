import fileinput
from functools import cache
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


def parse():
    ranges = []
    is_ingredient = False
    ingredients = []
    for line in get_input():
        if not line:
            is_ingredient = True
            continue
        if is_ingredient:
            ingredients.append(int(line))
        else:
            pairs = [int(i) for i in line.split("-")]
            ranges.append((pairs[0], pairs[1]))
    return ranges, ingredients


def is_overlap(r1: tuple[int, int], r2: tuple[int, int]) -> bool:
    # r1, r2 are sorted
    return r1[1] >= r2[0]


def merge_ranges(r1: tuple[int, int], r2: tuple[int, int]) -> tuple[int, int]:
    return (min(r1[0], r2[0]), max(r1[1], r2[1]))


@cache
def q1():
    count = 0
    ranges, ingredients = parse()
    for ing in ingredients:
        for lo, hi in ranges:
            if lo <= ing <= hi:
                count += 1
                break
    return count


@cache
def q2():
    ranges, _ = parse()
    while True:
        ranges = sorted(ranges)
        modified = False
        for i in range(1, len(ranges)):
            if is_overlap(ranges[i - 1], ranges[i]):
                merged_range = merge_ranges(ranges[i - 1], ranges[i])
                del ranges[i - 1]
                del ranges[i - 1]
                ranges.append(merged_range)
                modified = True
                break
        if not modified:
            break
    count = sum([hi - lo + 1 for lo, hi in ranges])
    return count


def main():
    print(q1())
    print(q2())
    assert q1() == 509
    assert q2() == 336790092076620


if __name__ == "__main__":
    main()
