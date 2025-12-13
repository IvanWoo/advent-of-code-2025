import fileinput
from dataclasses import dataclass
from functools import cache
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


@dataclass(frozen=True)
class Region:
    x: int
    y: int
    quantity: list[int]


def parse() -> tuple[dict[int, list[list[int]]], list[Region]]:
    shapes: dict[int, list[list[int]]] = {}
    regions: list[Region] = []
    idx = None
    shape: list[list[int]] = []
    for line in get_input():
        if len(shapes) < 6:
            if line == "":
                if idx is not None and shape:
                    shapes[idx] = shape
                idx = None
                shape = []
            else:
                if len(line) >= 2 and line[1] == ":":
                    idx = int(line[0])
                else:
                    shape.append([int(c == "#") for c in line])
        else:
            xy, quantity = line.split(": ")
            x, y = [int(part) for part in xy.split("x")]
            quantity = [int(part) for part in quantity.split(" ")]
            regions.append(Region(x, y, quantity))
    return shapes, regions


@cache
def q1():
    shapes, regions = parse()
    ret = 0
    for region in regions:
        size = region.x * region.y
        if size >= 9 * sum(region.quantity):
            ret += 1
        elif size < sum(
            [
                sum([sum(row) for row in shape]) * c
                for shape, c in zip(shapes.values(), region.quantity)
            ]
        ):
            ...
        else:
            print(f"HARD NP {shapes=} {regions=}")
    return ret


def main():
    print(q1())
    assert q1() == 583


if __name__ == "__main__":
    main()
