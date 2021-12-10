#!/usr/bin/env python3
"""Day 9: Smoke Basin

Usage: ./solution.py 1|2 FILE

"""

from __future__ import annotations

import sys
import typing as t
from argparse import ArgumentParser
from dataclasses import dataclass

verbose = False


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Grid:
    _width: int
    _height: int
    _values: list

    @classmethod
    def from_rows(cls, rows: list[list]) -> Grid:
        # trusting all rows are consistent length
        width = len(rows[0])
        height = len(rows)
        values = []
        for row in rows:
            values.extend(row)

        return cls(width, height, values)

    def __getitem__(self, item: Point):
        return self._values[item.y * self._width + item.x]

    def neighbors(self, point: Point) -> t.Iterator[Point]:
        pass


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
    pass


def part2(filename):
    pass


def read_file(filename):
    with open(filename, "r") as f:
        pass


if __name__ == "__main__":
    sys.exit(main())
