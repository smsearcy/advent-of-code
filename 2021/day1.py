import sys
import typing as t
from collections import defaultdict


def main():
    filename = sys.argv[1]
    action = sys.argv[2]
    depth_values = get_depths(filename)

    if action == "part1":
        print("Number of depth increases:", count_increases(depth_values))
    elif action == "part2":
        print("Number of sliding increases:", count_sliding_increases(depth_values))
    else:
        return "Invalid action"


def get_depths(filename) -> t.Iterator[int]:

    with open(filename, "r") as f:
        for line in f:
            yield int(line)


def count_increases(depths: t.Iterator[int]) -> int:
    depth_increases = 0
    current_depth = next(depths)
    for next_depth in depths:
        if next_depth > current_depth:
            depth_increases += 1
        current_depth = next_depth

    return depth_increases


def count_sliding_increases(depths: t.Iterable[int]) -> int:
    depths = list(depths)
    current_depth = sum(depths[0:3])
    print(f"{depths[0:3]}: {current_depth:,d}")

    count = defaultdict(int)

    for i in range(1, len(depths) - 2):
        next_depth = sum(depths[i : i + 3])
        print(f"{depths[i:i+3]}: {next_depth:,d}")
        if next_depth < current_depth:
            count["decreases"] += 1
        elif next_depth == current_depth:
            count["no change"] += 1
        elif next_depth > current_depth:
            count["increases"] += 1
        current_depth = next_depth

    print("Summary:", dict(count))

    return count["increases"]


if __name__ == "__main__":
    sys.exit(main())
