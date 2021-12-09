#!/usr/bin/env python3
"""Day 5: Hypothermal Venture

Usage: solution.py -v 1|2 input.txt

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

    @classmethod
    def from_string(cls, val) -> Point:
        x, y = val.split(",")
        return Point(int(x), int(y))


@dataclass
class Line:
    begin: Point
    end: Point

    def is_orthogonal(self) -> bool:
        return self.begin.x == self.end.x or self.begin.y == self.end.y

    def walk(self) -> t.Iterator[Point]:
        if self.is_orthogonal():
            if self.begin.x == self.end.x:
                start = min(self.begin.y, self.end.y)
                stop = max(self.begin.y, self.end.y)
                for y in range(start, stop + 1):
                    yield Point(self.begin.x, y)
            else:
                start = min(self.begin.x, self.end.x)
                stop = max(self.begin.x, self.end.x)
                for x in range(start, stop + 1):
                    yield Point(x, self.begin.y)
        else:
            # only need to deal with 45 degree angles
            if self.begin.x < self.end.x:
                x_range = range(self.begin.x, self.end.x + 1)
            else:
                x_range = reversed(range(self.end.x, self.begin.x + 1))
            if self.begin.y < self.end.y:
                y_range = range(self.begin.y, self.end.y + 1)
            else:
                y_range = reversed(range(self.end.y, self.begin.y + 1))
            for x, y in zip(x_range, y_range):
                yield Point(x, y)

    @property
    def max_width(self) -> int:
        return max((self.begin.x, self.end.x))

    @property
    def max_height(self) -> int:
        return max((self.begin.y, self.end.y))


@dataclass
class Ocean:
    map: list[list[int]]

    def score(self) -> int:
        score = 0
        for row in self.map:
            for val in row:
                if val > 1:
                    score += 1
        return score

    def __str__(self) -> str:
        output = []
        for row in self.map:
            line = ""
            for val in row:
                line += str(val) if val > 0 else "."
            output.append(line)
        return "\n".join(output)


def main():
    parser = ArgumentParser()
    parser.add_argument("part", type=int)
    parser.add_argument("filename")
    parser.add_argument("--verbose", "-v", action="store_true")

    global verbose
    args = parser.parse_args()
    action = args.part
    filename = args.filename
    if args.verbose:
        verbose = True

    if action == 1:
        lines = [line for line in read_file(filename) if line.is_orthogonal()]
        ocean = build_map(lines)
        print(ocean)
        print()
        print("Score:", ocean.score())

    elif action == 2:
        lines = list(read_file(filename))
        ocean = build_map(lines)
        print(ocean)
        print()
        print("Score:", ocean.score())

    else:
        return "Invalid action"


def read_file(filename) -> t.Iterator[Line]:
    with open(filename, "r") as f:
        for line in f:
            begin, end = line.strip().split(" -> ")
            yield Line(Point.from_string(begin), Point.from_string(end))


def build_map(lines: list[Line]) -> Ocean:
    width = max(line.max_width for line in lines) + 1
    height = max(line.max_height for line in lines) + 1

    row = [0] * width
    floor = []
    for y in range(height):
        floor.append(row.copy())

    for line in lines:
        if verbose:
            print(line)
        for point in line.walk():
            if verbose:
                print(point)
            floor[point.y][point.x] += 1

    return Ocean(floor)


if __name__ == "__main__":
    sys.exit(main())
