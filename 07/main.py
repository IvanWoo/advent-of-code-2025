import fileinput
from collections import defaultdict
from functools import cache
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


@cache
def q1():
    grid = list(get_input())
    nr, nc = len(grid), len(grid[0])
    count = 0
    beams = {grid[0].find("S")}
    for r in range(1, nr):
        for c in range(nc):
            if grid[r][c] == "^" and c in beams:
                count += 1
                beams.add(c - 1)
                beams.remove(c)
                beams.add(c + 1)
    return count


@cache
def q2():
    grid = list(get_input())
    nr, nc = len(grid), len(grid[0])
    beams = defaultdict(int)
    beams[grid[0].find("S")] = 1
    for r in range(1, nr):
        for c in range(nc):
            if grid[r][c] == "^" and c in beams:
                beams[c - 1] += beams[c]
                beams[c + 1] += beams[c]
                beams[c] = 0
    return sum(beams.values())


def main():
    print(q1())
    print(q2())
    assert q1() == 1566
    assert q2() == 5921061943075


if __name__ == "__main__":
    main()
