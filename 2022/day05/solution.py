#!/usr/bin/env python3
"""Template for Advent of Code solution in Python.

Usage: ./solution.py 1|2 FILE

"""

from __future__ import annotations

import re
import sys
from argparse import ArgumentParser
from collections import deque
from dataclasses import dataclass
from pathlib import Path

verbose = False


@dataclass
class Instruction:
    quantity: int
    source: int
    destination: int

    @classmethod
    def load(cls, value: str) -> Instruction:
        match = re.match(r"^move (\d+) from (\d) to (\d)", value)
        return Instruction(
            quantity=int(match[1]),
            source=int(match[2]),
            destination=int(match[3]),
        )


@dataclass
class SupplyYard:
    stacks: dict[int, deque[str]]

    def process1(self, instruction: Instruction):
        for i in range(instruction.quantity):
            crate = self.stacks[instruction.source].pop()
            self.stacks[instruction.destination].append(crate)

    def process2(self, instruction: Instruction):
        crates = []
        for i in range(instruction.quantity):
            crates.append(self.stacks[instruction.source].pop())
        self.stacks[instruction.destination].extend(reversed(crates))

    def top_row(self) -> str:
        return "".join(stack[-1] for stack in self.stacks.values())

    @classmethod
    def load(cls, value: str) -> SupplyYard:
        lines = value.splitlines()
        stack_labels = [int(label) for label in lines[-1].split()]
        stacks = {label: deque() for label in stack_labels}

        for line in reversed(lines[:-1]):
            for label, stack in stacks.items():
                index = 1 + 4 * (label - 1)
                try:
                    crate = line[index].strip()
                except IndexError:
                    continue
                if crate:
                    stack.append(crate)
        return SupplyYard(stacks)


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
    supply_yard, instructions = read_file(filename)
    if verbose:
        print(supply_yard, instructions)

    for instruction in instructions:
        supply_yard.process1(instruction)

    print(supply_yard.top_row())


def part2(filename):
    supply_yard, instructions = read_file(filename)
    for instruction in instructions:
        supply_yard.process2(instruction)

    print(supply_yard.top_row())


def read_file(filename) -> tuple[SupplyYard, list[Instruction]]:
    data = Path(filename).read_text()
    stack_data = ""
    process_instructions = False
    instructions = []
    supply_yard = None

    for line in data.splitlines(keepends=True):
        if line.strip() == "":
            process_instructions = True
            supply_yard = SupplyYard.load(stack_data)
            continue
        elif not process_instructions:
            stack_data += line
            continue
        else:
            instructions.append(Instruction.load(line.strip()))

    return supply_yard, instructions


if __name__ == "__main__":
    sys.exit(main())
