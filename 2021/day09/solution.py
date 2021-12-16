#!/usr/bin/env python3
"""Day 9: Smoke Basin

Usage: ./solution.py 1|2 FILE

"""

from __future__ import annotations

import itertools
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
    _values: list

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
        return (Point(x, y) for x in range(self._width) for y in range(self._height))

    def neighbors(self, point: Point) -> t.Iterator[Point]:
        """Yield the orthogonal neighbors to a particular point."""
        for delta in (-1, 1):
            if 0 <= point.x + delta < self._width:
                yield Point(point.x + delta, point.y)
            if 0 <= point.y + delta < self._height:
                yield Point(point.x, point.y + delta)

    def __str__(self):
        cols = [iter(self._values)] * self._width
        output = ["".join(str(val) for val in row) for row in zip(*cols)]
        return "\n".join(output)


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
    """Score based on lowest points."""
    grid = read_file(filename)
    if verbose:
        print(grid)

    low_points = []
    for point in grid:
        value = grid[point]
        if value < min(grid[p] for p in grid.neighbors(point)):
            low_points.append(point)

    if verbose:
        print("Low points:", low_points)
    print("Score:", sum(grid[pt] + 1 for pt in low_points))


def part2(filename):
    """Score based on size of basins."""
    grid = read_file(filename)
    if verbose:
        print(grid)

    # Really, it's finding regions bounded by "9"s
    # but since we have the low points I think I'll start there
    low_points = []
    for point in grid:
        value = grid[point]
        if value < min(grid[p] for p in grid.neighbors(point)):
            low_points.append(point)

    regions = []
    for start in low_points:
        region = set()
        build_region(start, grid, region)
        regions.append(region)

    if verbose:
        for region in regions:
            print(f"Region ({len(region)}):", region)

    largest_regions = sorted(regions, key=lambda obj: len(obj))[-3:]
    if verbose:
        print(largest_regions)
    score = 1
    for region in largest_regions:
        score *= len(region)
    print("Score:", score)


def build_region(start: Point, grid: Grid, region: set[Point]):
    """Build the region by recursively iterating the neighbors."""
    if grid[start] == 9:
        return
    region.add(start)
    for point in grid.neighbors(start):
        if point in region:
            continue
        build_region(point, grid, region)
    return


def read_file(filename) -> Grid:
    with open(filename, "r") as f:
        return Grid.from_rows(([int(val) for val in line.strip()] for line in f))


if __name__ == "__main__":
    sys.exit(main())
