import fileinput
from functools import cache
from pathlib import Path
from collections import deque
from z3 import IntVector, Optimize, sat

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


def parse():
    manuals = []
    for line in get_input():
        target = ()
        ops = []
        joltage_target = []
        for part in line.split(" "):
            if part.startswith("["):
                target = tuple((c == "#" for c in part[1:-1]))
            elif part.startswith("("):
                ops.append(list(set([int(c) for c in part[1:-1].split(",")])))
            elif part.startswith("{"):
                joltage_target = tuple((int(c) for c in part[1:-1].split(",")))
        manuals.append((target, ops, joltage_target))
    return manuals


def nxt(state: tuple, op: list[int]) -> tuple:
    new_state = list(state)
    for i in op:
        new_state[i] = not new_state[i]
    return tuple(new_state)


def bfs(target: tuple, ops: list[list[int]]) -> int:
    seen = set()
    initial_state = tuple([False for _ in range(len(target))])
    q = deque([(initial_state, 0)])
    while q:
        curr_state, curr_steps = q.popleft()
        if curr_state == target:
            return curr_steps
        if curr_state in seen:
            continue
        seen.add(curr_state)
        for op in ops:
            nxt_state = nxt(curr_state, op)
            q.append((nxt_state, curr_steps + 1))
    return -1


@cache
def q1():
    manuals = parse()
    ret = 0
    for target, ops, _ in manuals:
        ret += bfs(target, ops)
    return ret


def nxt_2(state: tuple, op: list[int]) -> tuple:
    new_state = list(state)
    for i in op:
        new_state[i] += 1
    return tuple(new_state)


def bfs_2(target: tuple, ops: list[list[int]]) -> int:
    seen = set()
    initial_state = tuple([0 for _ in range(len(target))])
    q = deque([(initial_state, 0)])
    while q:
        curr_state, curr_steps = q.popleft()
        if curr_state == target:
            return curr_steps
        if curr_state in seen:
            continue
        if any((target[i] < curr_state[i] for i in range(len(target)))):
            continue
        seen.add(curr_state)
        for op in ops:
            nxt_state = nxt_2(curr_state, op)
            q.append((nxt_state, curr_steps + 1))
    return -1


# brute force: too slow
@cache
def q2_brute():
    manuals = parse()
    ret = 0
    for _, ops, joltage_target in manuals:
        ret += bfs_2(joltage_target, ops)
    return ret


def solve(target: tuple, ops: list[list[int]]) -> int:
    rows = len(target)
    cols = len(ops)
    x = IntVector("x", cols)
    A = []  # cols x rows
    for op in ops:
        A.append([1 if i in op else 0 for i in range(rows)])

    o = Optimize()
    for j in range(cols):
        o.add(x[j] >= 0)

    for i in range(rows):
        equation_sum = sum(x[j] * A[j][i] for j in range(cols))
        o.add(equation_sum == target[i])

    objective = sum(x)
    o.minimize(objective)

    if o.check() == sat:
        model = o.model()
        opt_val = model.evaluate(objective).as_long()
        return opt_val
    else:
        print("Unsatisfiable or Unknown")
        return -1


@cache
def q2():
    manuals = parse()
    ret = 0
    for _, ops, joltage_target in manuals:
        ret += solve(joltage_target, ops)
    return ret


def main():
    print(q1())
    print(q2())
    assert q1() == 422
    assert q2() == 16361


if __name__ == "__main__":
    main()
