import fileinput
from collections import defaultdict, deque
from functools import cache
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


def parse() -> dict[str, set[str]]:
    connections = defaultdict(set)
    for line in get_input():
        start, ends = line.split(": ")
        connections[start] |= set([e for e in ends.split(" ")])
    return connections


# bfs
@cache
def q1():
    connections = parse()
    start = "you"
    end = "out"
    ret = 0
    q = deque([start])
    while q:
        curr = q.popleft()
        if curr == end:
            ret += 1
            continue
        for nxt in connections.get(curr, set()):
            q.append(nxt)
    return ret


# dfs tracking path: too slow
@cache
def q2_dfs():
    connections = parse()
    start = "svr"
    end = "out"
    ret = 0
    stack: deque[tuple[str, ...]] = deque([(start,)])
    seen = set()
    while stack:
        curr_path = stack.pop()
        if curr_path in seen:
            continue
        seen.add(curr_path)
        if curr_path and curr_path[-1] == end:
            if "dac" in curr_path and "fft" in curr_path:
                ret += 1
            continue
        for nxt in connections.get(curr_path[-1], set()):
            if nxt not in curr_path:
                new_path = tuple(list(curr_path) + [nxt])
                if new_path not in seen:
                    stack.append(new_path)
    return ret


@cache
def q2():
    connections = parse()

    @cache
    def path_count(
        start: str,
        end: str,
        visited_dac: bool = False,
        visited_fft: bool = False,
    ) -> int:
        if start == end:
            return int(visited_dac and visited_fft)

        if start == "dac":
            visited_dac = True
        elif start == "fft":
            visited_fft = True

        return sum(
            (
                path_count(nxt, end, visited_dac, visited_fft)
                for nxt in connections.get(start, set())
            )
        )

    start = "svr"
    end = "out"
    return path_count(start, end)


def main():
    print(q1())
    print(q2())
    assert q1() == 539
    assert q2() == 413167078187872


if __name__ == "__main__":
    main()
