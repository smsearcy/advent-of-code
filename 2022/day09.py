#!/usr/bin/env python3
"""Template for Advent of Code solution in Python.

Usage: ./day##.py [--verbose]

"""

from __future__ import annotations

import enum
import sys
from argparse import ArgumentParser
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

import pytest

verbose = False


class Direction(enum.Enum):
    UP = "U"
    LEFT = "L"
    DOWN = "D"
    RIGHT = "R"


@dataclass(frozen=True)
class Point:
    """Coordinate system with 0,0 in lower left."""

    x: int
    y: int

    def copy(self) -> Point:
        return Point(self.x, self.y)

    def move_up(self) -> Point:
        return Point(self.x, self.y + 1)

    def move_right(self) -> Point:
        return Point(self.x + 1, self.y)

    def move_down(self) -> Point:
        return Point(self.x, self.y - 1)

    def move_left(self) -> Point:
        return Point(self.x - 1, self.y)

    def check_adjacent(self, other: Point) -> bool:
        """See if two points are adjacent."""
        if other.x < self.x - 1 or self.x + 1 < other.x:
            return False
        if other.y < self.y - 1 or self.y + 1 < other.y:
            return False
        return True

    def follow(self, other: Point) -> Point:
        """Move to follow the other point."""
        if self.check_adjacent(other):
            return self
        new_location = self.copy()
        if self.x < other.x:
            new_location = new_location.move_right()
        elif self.x > other.x:
            new_location = new_location.move_left()
        if self.y < other.y:
            new_location = new_location.move_up()
        elif self.y > other.y:
            new_location = new_location.move_down()
        return new_location


def main():
    parser = ArgumentParser()
    parser.add_argument("--verbose", "-v", action="store_true")

    global verbose
    args = parser.parse_args()
    if args.verbose:
        verbose = True

    # the download script doesn't add the leading 0
    day = int(Path(__file__).stem.removeprefix("day"))
    input_file = Path(f"day{day}-input.txt")
    print(f"Reading input from {input_file}")
    puzzle_input = input_file.read_text()
    print(f"Day #{day} part 1 solution:", part1(puzzle_input))
    print(f"Day #{day} part 2 solution:", part2(puzzle_input))


def part1(puzzle_input: str):
    head = Point(0, 0)
    tail = Point(0, 0)
    visited = set()

    for instruction in parse_input(puzzle_input):
        match instruction:
            case Direction.UP, distance:
                for step in range(distance):
                    head = head.move_up()
                    tail = tail.follow(head)
                    visited.add(tail)
            case Direction.RIGHT, distance:
                for step in range(distance):
                    head = head.move_right()
                    tail = tail.follow(head)
                    visited.add(tail)
            case Direction.DOWN, distance:
                for step in range(distance):
                    head = head.move_down()
                    tail = tail.follow(head)
                    visited.add(tail)
            case Direction.LEFT, distance:
                for step in range(distance):
                    head = head.move_left()
                    tail = tail.follow(head)
                    visited.add(tail)
    return len(visited)


def part2(puzzle_input: str):
    rope = [Point(0, 0) for _ in range(10)]
    visited = {rope[9]}

    def update_rope(direction_):
        # in hindsight, I should have use functions so I could map directions to movement
        match direction_:
            case Direction.UP:
                rope[0] = rope[0].move_up()
            case Direction.RIGHT:
                rope[0] = rope[0].move_right()
            case Direction.DOWN:
                rope[0] = rope[0].move_down()
            case Direction.LEFT:
                rope[0] = rope[0].move_left()
        for knot in range(1, len(rope)):
            rope[knot] = rope[knot].follow(rope[knot - 1])

    for direction, distance in parse_input(puzzle_input):
        for step in range(distance):
            update_rope(direction)
            visited.add(rope[9])
        if verbose:
            print(rope)
    return len(visited)


def parse_input(puzzle_input: str) -> Iterator[tuple[Direction, int]]:
    for line in puzzle_input.splitlines():
        direction, distance = line.split()
        yield Direction(direction), int(distance)


SAMPLE = """
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
""".lstrip(
    "\n"
)

SAMPLE2 = """
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
""".lstrip(
    "\n"
)


@pytest.mark.parametrize(
    ("func", "input_", "expected"),
    [
        (part1, SAMPLE, 13),
        (part2, SAMPLE, 1),
        (part2, SAMPLE2, 36),
    ],
)
def test_solutions(func, input_, expected):
    global verbose
    verbose = True
    assert func(input_) == expected


if __name__ == "__main__":
    sys.exit(main())
