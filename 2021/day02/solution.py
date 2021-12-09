"""Advent of Code 2021: Day 2 - 'Dive'

Figure out where the submarine will end up.

"""

from __future__ import annotations

import sys
import typing as t


def main():
    filename = sys.argv[1]
    action = sys.argv[2]
    commands = get_directions(filename)

    if action == "part1":
        distance, depth = position_part1(commands)
        print(
            f"Distance: {distance:,d}; Depth: {depth:,d}; Product: {distance * depth:d}"
        )

    elif action == "part2":
        distance, depth = position_part2(commands)
        print(
            f"Distance: {distance:,d}; Depth: {depth:,d}; Product: {distance * depth:d}"
        )

    else:
        return "Invalid action"


def get_directions(filename) -> t.Iterator[tuple[str, int]]:

    with open(filename, "r") as f:
        for line in f:
            command, amount = line.split(" ", maxsplit=1)
            yield command, int(amount)


def position_part1(commands: t.Iterable[tuple[str, int]]) -> tuple[int, int]:
    """Returns the horizontal position and depth after processing commands.

    Directions: forward, down, up

    """

    position = depth = 0

    for direction, amount in commands:
        if direction == "up":
            amount = -amount
        if direction == "forward":
            position += amount
        else:
            depth += amount

    return position, depth


def position_part2(commands: t.Iterable[tuple[str, int]]) -> tuple[int, int]:
    """Returns the horizontal position and depth after processing commands.

    But now it tracks the "aim".

    Directions: forward, down, up

    """

    position = depth = aim = 0

    for direction, amount in commands:
        if direction == "up":
            aim -= amount
        elif direction == "down":
            aim += amount
        else:
            position += amount
            depth += aim * amount

    return position, depth


if __name__ == "__main__":
    sys.exit(main())
