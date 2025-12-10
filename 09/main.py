import fileinput
from functools import cache
from pathlib import Path
from dataclasses import dataclass

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


@dataclass(frozen=True)
class Position:
    c: int
    r: int


def parse() -> list[Position]:
    ps = []
    for line in get_input():
        c, r = line.split(",")
        ps.append(Position(c=int(c), r=int(r)))
    return ps


def calculate_area(p1: Position, p2: Position) -> int:
    return (abs(p1.c - p2.c) + 1) * (abs(p1.r - p2.r) + 1)


@cache
def q1():
    ps = parse()
    max_area = 0
    for i in range(len(ps)):
        for j in range(i + 1, len(ps)):
            area = calculate_area(ps[i], ps[j])
            max_area = max(max_area, area)
    return max_area


def in_polygon(seg: tuple[Position, Position], ps: list[Position]) -> bool:
    n = len(ps)
    sp1, sp2 = seg
    for i in range(n):
        diff_1 = diff_2 = 0
        j = (i + 1) % n
        p1, p2 = ps[i], ps[j]
        if p1.r == p2.r:
            min_c, max_c = min(p1.c, p2.c), max(p1.c, p2.c)
            if min_c <= sp1.c <= max_c or min_c <= sp2.c <= max_c:
                diff_1 = sp1.r - p1.r
                diff_2 = sp2.r - p1.r
        elif p1.c == p2.c:
            min_r, max_r = min(p1.r, p2.r), max(p1.r, p2.r)
            if min_r <= sp1.r <= max_r or min_r <= sp2.r <= max_r:
                diff_1 = sp1.c - p1.c
                diff_2 = sp2.c - p1.c
        else:
            print(f"invalid input: {p1=}, {p2=}")
        if diff_1 == 0 or diff_2 == 0:
            continue
        if diff_1 / diff_2 < 0:
            # intersect
            return False
    return True


@cache
def q2():
    ps = parse()
    max_area = 0
    for i in range(len(ps)):
        for j in range(i + 1, len(ps)):
            p1, p2 = ps[i], ps[j]
            if in_polygon((p1, p2), ps):
                area = calculate_area(p1, p2)
                max_area = max(max_area, area)
    return max_area


def main():
    print(q1())
    print(q2())
    assert q1() == 4773451098
    assert q2() == 1429075575


if __name__ == "__main__":
    main()
