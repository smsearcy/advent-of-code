#!/usr/bin/env python3
"""Template for Advent of Code solution in Python.

Usage: ./day##.py [--verbose]

"""

from __future__ import annotations

import itertools
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
    register = 1
    current_instruction = None
    instructions = parse_input(puzzle_input)
    signal_strength = 0

    for cycle in range(1, 221):
        if (cycle - 20) % 40 == 0:
            signal_strength += cycle * register

        if current_instruction is None:
            current_instruction = next(instructions).split()
        else:
            register += int(current_instruction[1])
            current_instruction = None
        if current_instruction == ["noop"]:
            current_instruction = None

    return signal_strength


def part2(puzzle_input: str):
    register = 1
    current_instruction = None
    instructions = parse_input(puzzle_input)
    display = "\n"

    for row in range(1, 7):
        for column in range(0, 40):
            if register - 1 <= column <= register + 1:
                display += "#"
            else:
                display += "."

            if current_instruction is None:
                current_instruction = next(instructions).split()
            else:
                register += int(current_instruction[1])
                current_instruction = None
            if current_instruction == ["noop"]:
                current_instruction = None
        display += "\n"

    return display


def parse_input(puzzle_input: str):
    yield from puzzle_input.splitlines()


SAMPLE = """
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
""".lstrip(
    "\n"
)


SAMPLE_DISPLAY = """
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
"""


@pytest.mark.parametrize(
    ("func", "input_", "expected"),
    [
        (part1, SAMPLE, 13140),
        (part2, SAMPLE, SAMPLE_DISPLAY),
    ],
)
def test_solutions(func, input_, expected):
    global verbose
    verbose = True
    assert func(input_) == expected


if __name__ == "__main__":
    sys.exit(main())
