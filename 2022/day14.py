#!/usr/bin/env python3
"""Template for Advent of Code solution in Python.

Usage: ./day##.py [--verbose]

"""

from __future__ import annotations

import sys
from argparse import ArgumentParser
from collections import UserDict
from collections.abc import Iterator
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path

import pytest
from utils import Point

verbose = False


@dataclass
class Cave(UserDict):
    def __init__(self, initial_data=None):
        super().__init__(initial_data)

    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except KeyError:
            if (
                self.left_edge <= item.x <= self.right_edge
                and 0 <= item.y <= self.bottom_edge
            ):
                return "."
            raise

    @cached_property
    def left_edge(self):
        return min(point.x for point in self.data.keys())

    @cached_property
    def right_edge(self) -> int:
        return max(point.x for point in self.data.keys())

    @cached_property
    def bottom_edge(self) -> int:
        return max(point.y for point in self.data.keys())

    def __str__(self):
        output = ""
        for y in range(0, self.bottom_edge + 1):
            for x in range(self.left_edge, self.right_edge + 1):
                output += self[Point(x, y)]
            output += "\n"
        return output


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
    cave = Cave()
    cave[Point(500, 0)] = "+"
    for rocks in parse_input(puzzle_input):
        for point in rocks:
            cave[point] = "#"
    if verbose:
        print(cave)
    return


def part2(puzzle_input: str):
    return


def parse_input(puzzle_input: str) -> Iterator[list[Point]]:
    for line in puzzle_input.splitlines():
        vertices = [Point.load(point) for point in line.split(" -> ")]
        points = []
        for index in range(1, len(vertices)):
            points += Point.line(vertices[index - 1], vertices[index])
        yield points


SAMPLE = """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
""".lstrip(
    "\n"
)


@pytest.mark.parametrize(
    ("func", "input_", "expected"),
    [
        (part1, SAMPLE, 24),
        (part2, SAMPLE, None),
    ],
)
def test_solutions(func, input_, expected):
    global verbose
    verbose = True
    assert func(input_) == expected


if __name__ == "__main__":
    sys.exit(main())
