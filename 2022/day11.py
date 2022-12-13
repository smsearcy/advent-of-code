#!/usr/bin/env python3
"""Template for Advent of Code solution in Python.

Usage: ./day##.py [--verbose]

"""

from __future__ import annotations

import re
import sys
from argparse import ArgumentParser
from collections import deque
from collections.abc import Callable
from dataclasses import dataclass
from operator import attrgetter
from pathlib import Path

import pytest

verbose = False


@dataclass
class Monkey:
    number: int
    items: deque[int]
    operation: Callable[[int], int]
    divide_by: int
    true_monkey: int
    false_monkey: int
    item_count: int = 0


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
    monkeys = parse_input(puzzle_input)

    for _ in range(20):
        if verbose:
            print(monkeys)
        for monkey in monkeys.values():
            while monkey.items:
                monkey.item_count += 1
                item = monkey.items.popleft()
                item = monkey.operation(item) // 3
                if item % monkey.divide_by == 0:
                    monkeys[monkey.true_monkey].items.append(item)
                else:
                    monkeys[monkey.false_monkey].items.append(item)

    active_monkeys = sorted(
        monkeys.values(), key=attrgetter("item_count"), reverse=True
    )
    return active_monkeys[0].item_count * active_monkeys[1].item_count


def part2(puzzle_input: str):
    monkeys = parse_input(puzzle_input)

    for _ in range(10000):
        for monkey in monkeys.values():
            while monkey.items:
                monkey.item_count += 1
                item = monkey.items.popleft()
                item = monkey.operation(item)
                if item % monkey.divide_by == 0:
                    monkeys[monkey.true_monkey].items.append(item)
                else:
                    monkeys[monkey.false_monkey].items.append(item)

    active_monkeys = sorted(
        monkeys.values(), key=attrgetter("item_count"), reverse=True
    )
    return active_monkeys[0].item_count * active_monkeys[1].item_count


def parse_input(puzzle_input: str) -> dict[int, Monkey]:
    data = puzzle_input.splitlines()
    monkeys = {}
    for idx in range(0, len(data), 7):
        monkey = parse_monkey(data[idx : idx + 7])
        monkeys[monkey.number] = monkey
    return monkeys


def parse_monkey(lines: list[str]) -> Monkey:
    number = re.match(r"Monkey (\d+):", lines[0])[1]
    items = f"[{lines[1].removeprefix('  Starting items: ')}]"
    operation = lines[2].removeprefix("  Operation: new = ")
    divide_by = re.search(r"divisible by (\d+)$", lines[3])[1]
    true_monkey = re.search(r"monkey (\d+)$", lines[4])[1]
    false_monkey = re.search(r"monkey (\d+)$", lines[5])[1]

    return Monkey(
        number=int(number),
        items=deque(eval(items)),
        operation=lambda old: eval(operation),
        divide_by=int(divide_by),
        true_monkey=int(true_monkey),
        false_monkey=int(false_monkey),
    )


SAMPLE = """
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
""".lstrip(
    "\n"
)


@pytest.mark.parametrize(
    ("func", "input_", "expected"),
    [
        (part1, SAMPLE, 10605),
        (part2, SAMPLE, 2713310158),
    ],
)
def test_solutions(func, input_, expected):
    global verbose
    verbose = True
    assert func(input_) == expected


if __name__ == "__main__":
    sys.exit(main())
