#!/usr/bin/env python3
"""Template for Advent of Code solution in Python.

Usage: solution.py input.txt 1|2

"""

from __future__ import annotations

import sys


def main():
    filename = sys.argv[1]
    action = sys.argv[2]

    # read_file(filename)

    if action == "1":
        pass

    elif action == "2":
        pass

    else:
        return "Invalid action"


def read_file(filename):
    with open(filename, "r") as f:
        pass


def part1():
    pass


if __name__ == "__main__":
    sys.exit(main())
