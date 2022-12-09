#!/usr/bin/env python3
"""Day 13: Transparent Origami

Usage: ./solution.py 1|2 FILE

"""

from __future__ import annotations

import re
import sys
import typing as t
from argparse import ArgumentParser
from dataclasses import dataclass, field

verbose = False


@dataclass(frozen=True)
class Point:
    x: int
    y: int


P = Point


@dataclass
class Grid:
    _width: int
    _height: int
    _values: list = field(repr=False)

    def fold_left(self, fold: int) -> Grid:
        values = []
        for y in range(0, self._height):
            for x1, x2 in zip(range(0, fold), range(self._width - 1, fold, -1)):
                values.append(self[P(x1, y)] | self[P(x2, y)])
        return Grid(fold, self._height, values)

    def fold_up(self, fold: int) -> Grid:
        values = []
        for y1, y2 in zip(range(0, fold), range(self._height - 1, fold, -1)):
            for x in range(0, self._width):
                values.append(self[P(x, y1)] | self[P(x, y2)])
        return Grid(self._width, fold, values)

    def __getitem__(self, item: Point):
        try:
            return self._values[item.y * self._width + item.x]
        except IndexError:
            print(self._width, self._height, len(self._values))
            raise IndexError(f"Not inside grid: {item}") from None

    def __setitem__(self, item: Point, value):
        try:
            self._values[item.y * self._width + item.x] = value
        except IndexError:
            raise IndexError(f"Not inside grid: {item}") from None

    def __iter__(self):
        return (Point(x, y) for x in range(self._width) for y in range(self._height))

    def __str__(self):
        cols = [iter(self._values)] * self._width
        output = ["".join("#" if val else "." for val in row) for row in zip(*cols)]
        return "\n".join(output)


@dataclass
class Fold:
    x: int | None = None
    y: int | None = None


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
    grid, folds = read_file(filename)
    if verbose:
        print(str(grid) + "\n")
        print(folds)
    else:
        print(f"{grid!r}\n")
        print(folds)

    for fold in folds[:1]:
        if fold.x:
            grid = grid.fold_left(fold.x)
        else:
            grid = grid.fold_up(fold.y)
        if verbose:
            print(f"{grid}\n")

    print("Score:", sum(1 for pt in grid if grid[pt]))


def part2(filename):
    grid, folds = read_file(filename)
    if verbose:
        print(str(grid) + "\n")
        print(folds)
    else:
        print(f"{grid!r}\n")
        print(folds)

    for fold in folds:
        if fold.x:
            grid = grid.fold_left(fold.x)
        else:
            grid = grid.fold_up(fold.y)
        if verbose:
            print(f"{grid}\n")

    print(grid)


def read_file(filename) -> tuple[Grid, list[Fold]]:
    dots = []
    folds = []
    with open(filename, "r") as f:
        for line in f:
            if "," in line:
                x, y = (int(val) for val in line.strip().split(","))
                dots.append(Point(x, y))
            elif match := re.match(r"fold along (x|y)=(\d+)", line):
                if match[1] == "x":
                    folds.append(Fold(x=int(match[2])))
                else:
                    folds.append(Fold(y=int(match[2])))
    width = height = 0
    for fold in folds:
        if not width and fold.x:
            width = fold.x * 2 + 1
        elif not height and fold.y:
            height = fold.y * 2 + 1
    grid = Grid(width, height, [0] * width * height)
    for dot in dots:
        grid[dot] = 1

    return grid, folds


if __name__ == "__main__":
    sys.exit(main())
