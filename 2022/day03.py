#!/usr/bin/env python3
"""Template for Advent of Code solution in Python.

Usage: ./solution.py 1|2 FILE

"""

from __future__ import annotations

import sys
from argparse import ArgumentParser
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from string import ascii_letters

verbose = False


PRIORITY_MAP = {letter: idx for idx, letter in enumerate(ascii_letters, start=1)}


@dataclass
class Rucksack:
    compartments: tuple[str, str]

    @property
    def items(self) -> str:
        return "".join(self.compartments)

    def duplicate(self) -> str:
        return "".join(set(self.compartments[0]).intersection(self.compartments[1]))


def main():
    parser = ArgumentParser()
    parser.add_argument("part", type=int)
    parser.add_argument("filename")
    parser.add_argument("--verbose", "-v", action="store_true")

    global verbose
    args = parser.parse_args()
    filename = Path(args.filename)
    if args.verbose:
        verbose = True

    if args.part == 1:
        part1(filename)
    elif args.part == 2:
        part2(filename)
    else:
        return f"Invalid 'part' specified: {args.part}"


def part1(filename: Path):
    total = 0
    for rucksack in read_file(filename):
        total += PRIORITY_MAP[rucksack.duplicate()]
    print(total)


def part2(filename: Path):
    # grouper recipe
    rucksacks = read_file(filename)
    groups = [iter(rucksacks)] * 3
    total = 0
    for group in zip(*groups):
        elves = list(group)
        badge = (
            set(elves[0].items)
            .intersection(elves[1].items)
            .intersection(elves[2].items)
        )
        total += PRIORITY_MAP[badge.pop()]

    print(total)


def read_file(filename: Path) -> Iterator[Rucksack]:
    data = filename.read_text()
    for line in data.splitlines():
        compartment_size = len(line) // 2
        yield Rucksack((line[:compartment_size], line[compartment_size:]))


if __name__ == "__main__":
    sys.exit(main())
