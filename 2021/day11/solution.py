#!/usr/bin/env python3
"""Day 11: Dumbo Octopus

Usage: ./solution.py 1|2 FILE

"""

from __future__ import annotations

import sys
import typing as t
from argparse import ArgumentParser
from dataclasses import dataclass

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
    _values: list[Octopus]

    @classmethod
    def from_rows(cls, rows: t.Iterable[t.Sequence]) -> Grid:
        # trusting all rows are consistent length
        width = None
        height = 0
        values = []
        for row in rows:
            height += 1
            if width is None:
                width = len(row)
            elif len(row) != width:
                raise ValueError("Rows need to have same length")
            values.extend(row)
        return cls(width, height, values)

    def __getitem__(self, item: Point):
        try:
            return self._values[item.y * self._width + item.x]
        except IndexError:
            raise IndexError(f"Not inside grid: {item}") from None

    def __iter__(self):
        return (Point(x, y) for y in range(self._height) for x in range(self._width))

    def neighbors(self, point: Point, *, diagonal: bool = False) -> t.Iterator[Point]:
        """Yield the neighbors to a particular point."""
        for delta in (-1, 1):
            if 0 <= point.x + delta < self._width:
                yield Point(point.x + delta, point.y)
            if 0 <= point.y + delta < self._height:
                yield Point(point.x, point.y + delta)

        if diagonal:
            for delta_x in (-1, 1):
                if point.x + delta_x < 0 or point.x + delta_x >= self._width:
                    continue
                for delta_y in (-1, 1):
                    if point.y + delta_y < 0 or point.y + delta_y >= self._height:
                        continue
                    yield Point(point.x + delta_x, point.y + delta_y)

    def flashes(self) -> int:
        return sum(1 for octopus in self._values if octopus.flashed)

    def all_flashed(self) -> bool:
        return self.flashes() == len(self._values)

    def reset(self):
        for octopus in self._values:
            octopus.reset()

    def __str__(self):
        cols = [iter(self._values)] * self._width
        output = ["".join(str(val) for val in row) for row in zip(*cols)]
        return "\n".join(output)


@dataclass
class Octopus:
    energy: int
    flashed: bool = False

    def increase(self) -> bool:
        if self.flashed:
            # short-circuit so it doesn't flash twice
            return False
        self.energy += 1
        if self.energy > 9:
            self.flashed = True
        return self.flashed

    def reset(self):
        if not self.flashed:
            return
        self.flashed = False
        self.energy = 0

    def __str__(self):
        return str(self.energy)


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
    """Count the number of flashes."""
    grid = read_file(filename)
    if verbose:
        print(grid)
        print()

    flash_count = 0
    for idx in range(100):
        flash_count += step(grid)
        if verbose and (idx < 10 or idx % 10 == 9):
            print(grid)
            print()

    print("Score:", flash_count)


def step(grid: Grid) -> int:
    """Advance the grid once, returning the number of octopuses that flashed."""
    for pt in grid:
        if grid[pt].increase():
            cascade(grid, pt)
    flash_count = grid.flashes()
    grid.reset()
    return flash_count


def cascade(grid: Grid, point: Point):
    for neighbor in grid.neighbors(point, diagonal=True):
        if grid[neighbor].increase():
            cascade(grid, neighbor)


def part2(filename):
    """When do they all flash?"""
    grid = read_file(filename)
    if verbose:
        print(grid)
        print()

    count = 1
    while True:
        for pt in grid:
            if grid[pt].increase():
                cascade(grid, pt)
        if grid.all_flashed():
            break
        grid.reset()
        count += 1

    print("Turn:", count)


def read_file(filename) -> Grid:
    with open(filename, "r") as f:
        return Grid.from_rows(
            ([Octopus(int(val)) for val in line.strip()] for line in f)
        )


if __name__ == "__main__":
    sys.exit(main())
