#!/usr/bin/env python3
"""Template for Advent of Code solution in Python.

Usage: ./solution.py 1|2 FILE

"""

from __future__ import annotations

import sys
from argparse import ArgumentParser
from collections.abc import Iterator
from dataclasses import dataclass, field
from operator import attrgetter
from pathlib import Path

verbose = False


@dataclass
class Directory:
    parent: Directory | None
    directories: dict[str, Directory] = field(default_factory=dict)
    files: list[File] = field(default_factory=list)

    @property
    def size(self) -> int:
        return sum(file.size for file in self.files) + sum(
            directory.size for directory in self.directories.values()
        )

    def walk(self) -> Iterator[Directory]:
        yield self
        for directory in self.directories.values():
            yield from directory.walk()


@dataclass
class File:
    name: str
    size: int


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
    root = read_file(filename)
    if verbose:
        print(root)
        print(root.size)

    total_size = 0
    for directory in root.walk():
        if directory.size > 100000:
            continue
        total_size += directory.size
    print(total_size)


def part2(filename):
    root = read_file(filename)
    drive_size = 70_000_000
    free_space = drive_size - root.size
    space_needed = 30_000_000 - free_space
    could_delete = []
    for directory in root.walk():
        if directory.size < space_needed:
            continue
        could_delete.append(directory)

    smallest_directory = sorted(could_delete, key=attrgetter("size"))[0]
    print(smallest_directory.size)


def read_file(filename) -> Directory:
    root = Directory(None)
    data = Path(filename).read_text()
    cwd = None
    for line in data.splitlines():
        match line.split():
            case ("$", "ls"):
                pass
            case ("$", "cd", "/"):
                cwd = root
            case ("$", "cd", ".."):
                cwd = cwd.parent
            case ("$", "cd", change_to):
                cwd = cwd.directories[change_to]
            case ("dir", dir_name):
                cwd.directories[dir_name] = Directory(cwd)
            case (size, filename):
                cwd.files.append(File(filename, int(size)))

    return root


if __name__ == "__main__":
    sys.exit(main())
