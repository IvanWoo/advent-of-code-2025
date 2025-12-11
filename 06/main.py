import fileinput
from functools import cache, reduce
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line


def parse(is_vertical: bool = False):
    grid = list(get_input())
    nr, nc = len(grid), len(grid[0])

    boundaries = [i for i, char in enumerate(grid[-1]) if char in "+*"]
    boundaries.append(nc - 1)

    problems = []
    for i in range(1, len(boundaries)):
        problem = []
        cl, cr = boundaries[i - 1], boundaries[i]
        if is_vertical:
            for c in range(cl, cr):
                str_num = ""
                for r in range(nr):
                    if grid[r][c].isdigit():
                        str_num += grid[r][c]
                if str_num:
                    problem.append(int(str_num))
        else:
            for r in range(nr):
                str_num = ""
                for c in range(cl, cr):
                    if grid[r][c].isdigit():
                        str_num += grid[r][c]
                if str_num:
                    problem.append(int(str_num))
        problem.append(grid[-1][cl])
        problems.append(problem)
    return problems


def calculate(problem) -> int:
    numbers, op = problem[:-1], problem[-1]
    return reduce(
        lambda x, y: (x + y) if op == "+" else (x * y), numbers, 0 if op == "+" else 1
    )


@cache
def q1():
    problems = parse()
    return sum(calculate(p) for p in problems)


@cache
def q2():
    problems = parse(is_vertical=True)
    return sum(calculate(p) for p in problems)


def main():
    print(q1())
    print(q2())
    assert q1() == 6172481852142
    assert q2() == 10188206723429


if __name__ == "__main__":
    main()
