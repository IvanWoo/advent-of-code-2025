import fileinput
import heapq
from dataclasses import dataclass
from functools import cache, reduce
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


@dataclass(frozen=True)
class Position:
    x: int
    y: int
    z: int


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


def distance(p1: Position, p2: Position) -> float:
    return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2 + (p1.z - p2.z) ** 2) ** 0.5


def find_in_groups(i: int, j: int, groups: list[set[int]]) -> tuple[int, int]:
    ig, jg = -1, -1
    for idx, g in enumerate(groups):
        if i in g:
            ig = idx
        if j in g:
            jg = idx
    assert ig != -1 or jg != -1
    return (ig, jg)


def is_connected(i: int, j: int, groups: list[set[int]]) -> bool:
    ig, jg = find_in_groups(i, j, groups)
    return ig == jg


def merge_groups(i: int, j: int, groups: list[set[int]]) -> list[set[int]]:
    ig, jg = find_in_groups(i, j, groups)
    merged_g = groups[ig] | groups[jg]
    new_groups = [g for idx, g in enumerate(groups) if idx not in {ig, jg}]
    new_groups.append(merged_g)
    return new_groups


def parse():
    ps: list[Position] = []
    for line in get_input():
        x, y, z = [int(part) for part in line.split(",")]
        ps.append(Position(x, y, z))
    return ps


@cache
def q1():
    positions = parse()
    groups: list[set[int]] = [{i} for i in range(len(positions))]
    dist_pq = []
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            heapq.heappush(dist_pq, (distance(positions[i], positions[j]), i, j))
    count = 0
    target = 1000
    while count < target:
        _, mi, mj = heapq.heappop(dist_pq)
        if not is_connected(mi, mj, groups):
            groups = merge_groups(mi, mj, groups)
        count += 1

    return reduce(lambda x, y: x * y, sorted([len(g) for g in groups])[-3:], 1)


@cache
def q2():
    positions = parse()
    groups: list[set[int]] = [{i} for i in range(len(positions))]
    dist_pq = []
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            heapq.heappush(dist_pq, (distance(positions[i], positions[j]), i, j))
    while len(groups) != 1:
        _, mi, mj = heapq.heappop(dist_pq)
        if not is_connected(mi, mj, groups):
            groups = merge_groups(mi, mj, groups)
    return positions[mi].x * positions[mj].x


def main():
    print(q1())
    print(q2())
    assert q1() == 72150
    assert q2() == 3926518899


if __name__ == "__main__":
    main()
