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

verbose = False


@dataclass
class Range:
    begin: int
    end: int

    def contains(self, other: Range):
        if self.begin <= other.begin and other.end <= self.end:
            return True
        else:
            return False

    def overlaps(self, other: Range):
        if self.end < other.begin:
            return False
        if other.end < self.begin:
            return False
        return True

    @classmethod
    def load(cls, value: str) -> Range:
        begin, end = value.split("-")
        return Range(int(begin), int(end))


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
    counter = 0
    for range1, range2 in read_file(filename):
        if range1.contains(range2) or range2.contains(range1):
            counter += 1
    print(counter)


def part2(filename: Path):
    counter = 0
    for range1, range2 in read_file(filename):
        if range1.overlaps(range2):
            if verbose:
                print(range1, range2)
            counter += 1
    print(counter)


def read_file(filename: Path) -> Iterator[tuple[Range, Range]]:
    data = filename.read_text()
    for line in data.splitlines():
        first, second = line.split(",")
        yield Range.load(first), Range.load(second)


if __name__ == "__main__":
    sys.exit(main())
