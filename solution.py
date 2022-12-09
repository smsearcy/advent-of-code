#!/usr/bin/env python3
"""Template for Advent of Code solution in Python.

Usage: ./day##.py [--verbose]

"""

from __future__ import annotations

import sys
from argparse import ArgumentParser
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

import pytest

verbose = False


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
    return


def part2(puzzle_input: str):
    return


def parse_input(puzzle_input: str):
    for line in puzzle_input.splitlines():
        pass


SAMPLE = """
""".lstrip(
    "\n"
)


@pytest.mark.parametrize(
    ("func", "input_", "expected"),
    [
        (part1, SAMPLE, 42),
        (part2, SAMPLE, 42),
    ],
)
def test_solutions(func, input_, expected):
    global verbose
    verbose = True
    assert func(input_) == expected


if __name__ == "__main__":
    sys.exit(main())
