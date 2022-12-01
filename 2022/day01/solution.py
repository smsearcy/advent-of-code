#!/usr/bin/env python3
"""Template for Advent of Code solution in Python.

Usage: ./solution.py 1|2 FILE

"""

from __future__ import annotations

import sys
from argparse import ArgumentParser
from dataclasses import dataclass, field
from collections.abc import Iterator

verbose = False


@dataclass
class ElfInventory:
    food: list[int] = field(default_factory=list)

    @property
    def calories(self) -> int:
        return sum(self.food)


def main():
    parser = ArgumentParser()
    parser.add_argument("part", type=int)
    parser.add_argument("filename")
    parser.add_argument("--verbose", "-v", action="store_true")

    global verbose
    args = parser.parse_args()
    filename = args.filename
    if args.verbose:
        verbose = True

    if args.part == 1:
        part1(filename)
    elif args.part == 2:
        part2(filename)
    else:
        return f"Invalid 'part' specified: {args.part}"


def part1(filename):
    elves = [elf for elf in read_file(filename)]
    if verbose:
        print(elves)

    most_calories = max(elf.calories for elf in elves)
    print("Most calories:", most_calories)


def part2(filename):
    elves = [elf for elf in read_file(filename)]
    calories = sorted((elf.calories for elf in elves), reverse=True)

    most_calories = calories[:3]
    print("Top 3:", most_calories)
    print("Total:", sum(most_calories))


def read_file(filename) -> Iterator[ElfInventory]:
    with open(filename, "r") as f:
        elf = ElfInventory()
        for line in f:
            if line.strip() == "":
                yield elf
                elf = ElfInventory()
                continue
            elf.food.append(int(line))
        yield elf


if __name__ == "__main__":
    sys.exit(main())
