#!/usr/bin/env python3
"""Day 15: Chiton

Finding the least risky path through the cave.

Usage: ./solution.py 1|2 FILE

"""

from __future__ import annotations

import sys
import typing as t
from argparse import ArgumentParser
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from multiprocessing import Process, Queue, cpu_count
from operator import attrgetter

verbose = False


@dataclass(frozen=True, slots=True)
class Point:
    x: int
    y: int


P = Point


@dataclass
class Grid:
    width: int
    height: int
    _values: list[int]

    @classmethod
    def from_rows(cls, rows: t.Iterable[t.Sequence]) -> Grid:
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
            return self._values[item.y * self.width + item.x]
        except IndexError:
            raise IndexError(f"Not inside grid: {item}") from None

    def __iter__(self):
        return (Point(x, y) for y in range(self.height) for x in range(self.width))

    def neighbors(self, point: Point) -> t.Iterator[Point]:
        """Yield the neighbors to a particular point."""
        for delta in (-1, 1):
            if 0 <= point.x + delta < self.width:
                yield Point(point.x + delta, point.y)
            if 0 <= point.y + delta < self.height:
                yield Point(point.x, point.y + delta)

    def __str__(self):
        cols = [iter(self._values)] * self.width
        output = ["".join(str(val) for val in row) for row in zip(*cols)]
        return "\n".join(output)


@dataclass
class Path:
    nodes: set[Point] = field(default_factory=set)
    end: Point | None = None
    score: int = 0

    @classmethod
    def start(cls, point: Point) -> Path:
        return cls({point}, point)

    def add(self, spot: Point, grid: Grid):
        if spot in self.nodes:
            raise ValueError("Cannot visit nodes twice")
        self.nodes.add(spot)
        self.end = spot
        self.score += grid[spot]

    def copy(self) -> Path:
        return Path(self.nodes.copy(), self.end, self.score)

    def draw(self, grid):
        output = ""
        row = 0
        for point in grid:
            if point.y != row:
                print(output)
                output = ""
                row = point.y
            if point in self.nodes:
                output += "."
            else:
                output += str(grid[point])
        print(output)

    def __str__(self):
        return f"End: {self.end}; Len: {len(self.nodes)}; Score: {self.score}"


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
        part1_parallel(filename)
    elif args.part == 2:
        part2(filename)
    else:
        return f"Invalid 'part' specified: {args.part}"


def part1(filename):
    """Trying to incorporate some improvements suggested by a coworker."""
    grid = read_file(filename)
    if verbose:
        print(grid)
        print()

    paths = deque((Path.start(P(0, 0)),))
    print(datetime.now())

    count = 0
    best_path = None
    while best_path is None:
        path = paths.popleft()

        count += 1
        if count % 10000 == 0:
            if verbose:
                print(f"{len(paths) + 1} ({path.score}); ", end="", flush=True)
            else:
                print(".", end="", flush=True)

        for point in grid.neighbors(path.end):
            if point in path.nodes:
                continue
            new_path = path.copy()
            new_path.add(point, grid)
            if new_path.end == P(grid.width - 1, grid.height - 1):
                # found the end
                best_path = new_path
                break
            paths.appendleft(new_path)

        paths = deque(sorted(paths, key=attrgetter("score")))

    print()
    print(datetime.now())
    print()
    if verbose:
        best_path.draw(grid)
        print()
    print("Best score:", best_path.score)


def part1_parallel(filename):
    """My original depth-first approach, with multiprocessing."""

    grid = read_file(filename)
    if verbose:
        print(grid)
        print()

    process_count = cpu_count()

    # use a list right now because this is going to be a short list
    paths = [Path.start(P(0, 0))]
    print(datetime.now())
    while len(paths) <= process_count:
        path = paths.pop()
        for point in grid.neighbors(path.end):
            if point in path.nodes:
                continue
            new_path = path.copy()
            new_path.add(point, grid)
            paths.append(new_path)

    print(f"Loaded {len(paths)} initial paths")
    processes = []
    que = Queue()
    for path in paths:
        p = Process(target=depth_first_subprocess, args=([path], grid, que))
        p.start()
        processes.append(p)

    results = []
    for _ in paths:
        results.append(que.get())

    for p in processes:
        p.join()

    best_path = sorted(results, key=attrgetter("score"))[0]

    print()
    print(datetime.now())
    print()
    if verbose:
        best_path.draw(grid)
        print()

    print("Overall best process:", best_path.score)


def depth_first_subprocess(paths: list[Path], grid: Grid, que: Queue):
    """Find the best path from the provided paths."""
    best_path = None

    paths = deque(paths)
    count = 0
    while len(paths) > 0:
        count += 1
        if count % 100000 == 0:
            if best_path is None:
                print(f"{len(paths)} (); ", end="", flush=True)
            else:
                print(f"{len(paths)} ({best_path.score}); ", end="", flush=True)

        path = paths.pop()
        for point in grid.neighbors(path.end):
            if point in path.nodes:
                continue
            new_path = path.copy()
            new_path.add(point, grid)
            if new_path.end == P(grid.width - 1, grid.height - 1):
                # found the end
                if best_path is None or new_path.score < best_path.score:
                    if verbose:
                        print("Found new best path:", new_path.score)
                    best_path = new_path
                continue
            elif best_path is not None and new_path.score >= best_path.score:
                continue
            paths.append(new_path)

    print("Best score for process:", best_path.score)
    que.put(best_path)


def part2(filename):
    pass


def read_file(filename) -> Grid:
    with open(filename, "r") as f:
        return Grid.from_rows(([int(val) for val in line.strip()] for line in f))


if __name__ == "__main__":
    sys.exit(main())
