#!/usr/bin/env python3
"""Day 6: Laternfish

Usage: ./solution.py 1|2 FILE

"""

from __future__ import annotations

import sys
import typing as t
from argparse import ArgumentParser
from dataclasses import dataclass

verbose = False


@dataclass
class Fish:
    cycle: int = 8

    def age(self) -> bool:
        """Advance this fish's age one day.

        Returns:
            True if produces a new fish

        """
        self.cycle -= 1
        if self.cycle < 0:
            self.cycle = 6
            return True
        return False

    def __str__(self):
        return str(self.cycle)


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
    fishes = [Fish(fish) for fish in read_file(filename)]
    print("Starting number of fish:", len(fishes))
    if verbose:
        print(fishes)
    for day in range(80):
        new_born = 0
        for fish in fishes:
            if fish.age():
                new_born += 1

        for i in range(new_born):
            fishes.append(Fish())

        if verbose:
            print(fishes)

    print("Final number of fish:", len(fishes))


def part2(filename):
    fish_per_day = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}
    for fish in read_file(filename):
        fish_per_day[fish] += 1

    print("Starting number of fish:", sum(fish_per_day.values()))
    if verbose:
        print(list(fish_per_day.values()))

    for day in range(256):
        old_fish = fish_per_day.copy()
        fish_per_day = {
            0: old_fish[1],
            1: old_fish[2],
            2: old_fish[3],
            3: old_fish[4],
            4: old_fish[5],
            5: old_fish[6],
            6: old_fish[7] + old_fish[0],
            7: old_fish[8],
            8: old_fish[0],
        }
        if verbose:
            print(list(fish_per_day.values()))

    print("Final number of fish:", sum(fish_per_day.values()))


def read_file(filename) -> t.Iterator[int]:
    with open(filename, "r") as f:
        line = f.readline()
    yield from (int(fish) for fish in line.split(","))


if __name__ == "__main__":
    sys.exit(main())
