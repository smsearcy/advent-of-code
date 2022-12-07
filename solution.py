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
        print("Part 1 solution:", part1(filename))
    elif args.part == 2:
        print("Part 2 solution:", part2(filename))
    else:
        return f"Invalid 'part' specified: {args.part}"


def part1(filename: Path):
    return


def part2(filename: Path):
    return


def read_file(filename: Path):
    data = filename.read_text()
    for line in data.splitlines():
        pass


if __name__ == "__main__":
    sys.exit(main())
