import fileinput
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
    rs, cs = len(grid), len(grid[0])
    count = 0
    for r in range(rs):
        for c in range(cs):
            if grid[r][c] != "@":
                continue
            total = 0
            for dr, dc in [
                (-1, -1),
                (-1, 0),
                (-1, 1),
                (0, -1),
                (0, 1),
                (1, -1),
                (1, 0),
                (1, 1),
            ]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rs and 0 <= nc < cs:
                    if grid[nr][nc] == "@":
                        total += 1
            if total < 4:
                count += 1
    return count


@cache
def q2():
    grid = list(get_input())
    rs, cs = len(grid), len(grid[0])
    count = 0
    removed = set()
    while True:
        _count = 0
        for r in range(rs):
            for c in range(cs):
                if grid[r][c] != "@" or (r, c) in removed:
                    continue
                total = 0
                for dr, dc in [
                    (-1, -1),
                    (-1, 0),
                    (-1, 1),
                    (0, -1),
                    (0, 1),
                    (1, -1),
                    (1, 0),
                    (1, 1),
                ]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rs and 0 <= nc < cs:
                        if grid[nr][nc] == "@" and (nr, nc) not in removed:
                            total += 1
                if total < 4:
                    _count += 1
                    removed.add((r, c))
        if _count:
            count += _count
        else:
            break
    return count


def main():
    print(q1())
    print(q2())
    assert q1() == 1464
    assert q2() == 8409


if __name__ == "__main__":
    main()
