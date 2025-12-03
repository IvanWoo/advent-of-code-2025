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
    ret = 0
    id_ranges = list(get_input())[0]
    for id_range in id_ranges.split(","):
        start, end = int(id_range.split("-")[0]), int(id_range.split("-")[1])
        for v in range(start, end + 1):
            sv = str(v)
            if len(sv) % 2 == 0:
                mid = len(sv) // 2
                if sv[:mid] == sv[mid:]:
                    ret += v
    return ret


@cache
def q2():
    ret = 0
    id_ranges = list(get_input())[0]
    for id_range in id_ranges.split(","):
        start, end = int(id_range.split("-")[0]), int(id_range.split("-")[1])
        for v in range(start, end + 1):
            sv = str(v)
            mid = len(sv) // 2
            for length in range(1, mid + 1):
                seq = sv[:length]
                sv_copy = sv
                while sv_copy:
                    if sv_copy.startswith(seq):
                        sv_copy = sv_copy[length:]
                    else:
                        break
                if sv_copy == "":
                    ret += v
                    break
    return ret


def main():
    print(q1())
    print(q2())
    assert q1() == 20223751480
    assert q2() == 30260171216


if __name__ == "__main__":
    main()
