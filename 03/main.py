import fileinput
from functools import cache
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


def _scan(seq: str, count: int, reverse: bool) -> int:
    seq = seq[::-1] if reverse else seq

    length = len(seq)
    i = 0
    ret = ""
    while len(ret) != count:
        if length - i == count - len(ret):
            ret += seq[i:]
            break
        mx = seq[i]
        mx_i = i
        for j in range(i, length - (count - len(ret)) + 1):
            if seq[j] > mx:
                mx = seq[j]
                mx_i = j
        ret += mx
        if mx_i != i:
            i = mx_i + 1
        else:
            i += 1

    ret = ret[::-1] if reverse else ret
    return int(ret)


def scan(seq: str, count: int) -> int:
    return max([_scan(seq, count, reverse) for reverse in [True, False]])


@cache
def q1():
    count = 2
    ret = 0
    for bank in get_input():
        ret += scan(bank, count)
    return ret


@cache
def q2():
    count = 12
    ret = 0
    for bank in get_input():
        ret += scan(bank, count)
    return ret


def main():
    print(q1())
    print(q2())
    assert q1() == 17095
    assert q2() == 168794698570517


if __name__ == "__main__":
    main()
