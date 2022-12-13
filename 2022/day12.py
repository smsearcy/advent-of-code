#!/usr/bin/env python3
"""Template for Advent of Code solution in Python.

Usage: ./day##.py [--verbose]

"""

from __future__ import annotations

import sys
from argparse import ArgumentParser
from collections import deque
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from string import ascii_lowercase

import pytest
from utils import Grid, Point

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
    terrain = parse_input(puzzle_input)

    starting_point = terrain.find("S")
    if verbose:
        print("Starting point:", starting_point)
    elevation = {letter: score for score, letter in enumerate(ascii_lowercase)}
    elevation["S"] = elevation["a"]
    elevation["E"] = elevation["z"]

    points_visited = {starting_point: 0}
    next_points = deque([starting_point])

    while next_points:
        point = next_points.pop()
        cost = points_visited[point] + 1
        height = elevation[terrain[point]]
        for neighbor in terrain.neighbors(point):
            if elevation[terrain[neighbor]] > height + 1:
                continue
            if neighbor in points_visited and points_visited[neighbor] <= cost:
                continue
            points_visited[neighbor] = cost
            next_points.append(neighbor)

    ending_point = terrain.find("E")
    return points_visited.get(ending_point)


def part2(puzzle_input: str):
    terrain = parse_input(puzzle_input)
    starting_point = terrain.find("S")
    if verbose:
        print("Starting point:", starting_point)
    elevation = {letter: score for score, letter in enumerate(ascii_lowercase)}
    elevation["S"] = elevation["a"]
    elevation["E"] = elevation["z"]

    shortest_trail = None
    starting_points = [terrain.find("S")]
    starting_points += terrain.find_all("a")
    for starting_point in starting_points:
        points_visited = {starting_point: 0}
        next_points = deque([starting_point])

        while next_points:
            point = next_points.pop()
            cost = points_visited[point] + 1
            if shortest_trail is not None and cost > shortest_trail:
                continue
            height = elevation[terrain[point]]
            for neighbor in terrain.neighbors(point):
                if terrain[neighbor] in {"S", "a"}:
                    # never enter the lowest level
                    continue
                if elevation[terrain[neighbor]] > height + 1:
                    continue
                if neighbor in points_visited and points_visited[neighbor] <= cost:
                    continue
                points_visited[neighbor] = cost
                next_points.append(neighbor)

        ending_point = terrain.find("E")
        if ending_point not in points_visited:
            continue
        trail_length = points_visited[ending_point]
        if shortest_trail is None:
            shortest_trail = trail_length
        elif trail_length < shortest_trail:
            shortest_trail = trail_length

    return shortest_trail


def parse_input(puzzle_input: str) -> Grid:
    elevations = [list(line) for line in puzzle_input.splitlines()]
    return Grid(elevations)


SAMPLE = """
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
""".lstrip(
    "\n"
)


@pytest.mark.parametrize(
    ("func", "input_", "expected"),
    [
        (part1, SAMPLE, 31),
        (part2, SAMPLE, 29),
    ],
)
def test_solutions(func, input_, expected):
    global verbose
    verbose = True
    assert func(input_) == expected


if __name__ == "__main__":
    sys.exit(main())
