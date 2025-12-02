import fileinput
from functools import cache
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


# simulation
def run_rotate(curr: int, rotate: str) -> tuple[int, int]:
    direction = rotate[0]
    distance = int(rotate[1:])
    count = 0
    for _ in range(distance):
        if direction == "L":
            curr -= 1
        else:
            curr += 1
        curr %= 100
        if curr == 0:
            count += 1
    return curr, count


@cache
def q1():
    count = 0
    curr = 50
    for rotate in get_input():
        if curr == 0:
            count += 1
        curr, _ = run_rotate(curr, rotate)
        # print(rotate, curr)
    return count


@cache
def q2():
    count = 0
    curr = 50
    for rotate in get_input():
        curr, _count = run_rotate(curr, rotate)
        # print(rotate, curr, _count)
        count += _count
    return count


def main():
    print(q1())
    print(q2())
    assert q1() == 1076
    assert q2() == 6379


if __name__ == "__main__":
    main()
