#!/usr/bin/env python3
"""Day 12: Passage Pathing

Usage: ./solution.py 1|2 FILE

"""

from __future__ import annotations

import sys
import typing as t
from argparse import ArgumentParser
from dataclasses import dataclass
from pprint import pprint

verbose = False


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
    """How many paths through the cave (visit small rooms only once)."""
    caves = read_file(filename)
    if verbose:
        pprint(caves)

    paths = find_path_part1(caves, "start", [])
    for path in paths:
        print(",".join(path))

    print("Total:", len(paths))


def find_path_part1(
    caves: dict[str, set[str]], start: str, path: list[str]
) -> list[list[str]]:
    """Recursively find a path starting in `start`, only visit small rooms once."""
    path.append(start)
    if start == "end":
        return [path]
    paths = []
    for room in caves[start]:
        if room.islower() and room in set(path):
            # skip small rooms we've already been in
            continue
        paths.extend(find_path_part1(caves, room, path.copy()))

    return paths


def part2(filename):
    """How many paths through the cave (visit small rooms only once)."""
    caves = read_file(filename)
    if verbose:
        pprint(caves)

    paths = find_path_part2(caves, "start", [])
    for path in paths:
        print(",".join(path))

    print("Total:", len(paths))


def find_path_part2(
    caves: dict[str, set[str]], start: str, path: list[str]
) -> list[list[str]]:
    """Recursively find a path starting in `start`, only visit *one* small cave twice."""
    path.append(start)
    if start == "end":
        return [path]
    paths = []
    for room in caves[start]:
        if room.islower() and room in set(path):
            # skip small rooms we've already been in
            continue
        paths.extend(find_path_part1(caves, room, path.copy()))

    return paths


def read_file(filename) -> dict[str, set[str]]:
    cave_graph = {}
    with open(filename, "r") as f:
        for line in f:
            room1, room2 = line.strip().split("-")
            if room1 != "end" and room2 != "start":
                cave_graph.setdefault(room1, set()).add(room2)
            if room1 != "start" and room2 != "end":
                cave_graph.setdefault(room2, set()).add(room1)
    return cave_graph


if __name__ == "__main__":
    sys.exit(main())
