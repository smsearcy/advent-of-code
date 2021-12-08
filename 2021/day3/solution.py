"""Advent of Code 2021: Day 3 - 'Binary Diagnostic'

Process binary diagnostic report.

"""

from __future__ import annotations

import sys
from dataclasses import dataclass


@dataclass
class Diagnostics:
    codes: list[str]

    def __len__(self) -> int:
        return len(self.codes)

    @property
    def code_size(self) -> int:
        return len(self.codes[0])

    def most_common(self, pos: int) -> str:
        ones_count = sum(1 for code in self.codes if code[pos] == "1")
        if ones_count >= len(self.codes) / 2:
            print(f"Most common: 1 ({ones_count}/{len(self.codes)}")
            return "1"
        else:
            print(f"Most common: 0 ({len(self.codes) - ones_count}/{len(self.codes)}")
            return "0"

    def least_common(self, pos: int) -> str:
        ones_count = sum(1 for code in self.codes if code[pos] == "1")
        if ones_count >= len(self.codes) / 2:
            print(f"Least common: 0 ({len(self.codes) - ones_count}/{len(self.codes)}")
            return "0"
        else:
            print(f"Least common: 1 ({ones_count}/{len(self.codes)}")
            return "1"

    def filter(self, pos: int, value: str) -> Diagnostics:
        return Diagnostics(codes=[code for code in self.codes if code[pos] == value])


def main():
    filename = sys.argv[1]
    action = sys.argv[2]
    diagnostics = read_file(filename)

    if action == "part1":
        gamma, epsilon = part1(diagnostics)
        print(f"Gamma: {gamma}; Epsilon: {epsilon}")
        print(f"Power consumption: {int(gamma, 2) * int(epsilon, 2)}")

    elif action == "part2":
        oxygen, co2 = part2(diagnostics)
        print(f"Oxygen: {oxygen}; C02: {co2}")
        print(f"Life Support: {int(oxygen, 2) * int(co2, 2)}")

    else:
        return "Invalid action"


def read_file(filename) -> Diagnostics:
    with open(filename, "r") as f:
        codes = Diagnostics(codes=[line.strip() for line in f])
    return codes


def part1(diagnostics: Diagnostics) -> tuple[str, str]:
    """Calculate Gamma and Epsilon values."""

    # these will be the inverse of each other
    gamma = ""  # most
    epsilon = ""  # least

    for idx in range(diagnostics.code_size):
        most_common = diagnostics.most_common(idx)
        if most_common == "1":
            gamma += "1"
            epsilon += "0"
        else:
            gamma += "0"
            epsilon += "1"

    return gamma, epsilon


def part2(diagnostics: Diagnostics) -> tuple[str, str]:
    """Calculate oxygen production and CO2 scrubbing."""

    # so I can reset the diagnostics (should I just pass the list of strings?)
    codes = [code for code in diagnostics.codes]

    # Get the oxygen value
    for idx in range(diagnostics.code_size):
        value = diagnostics.most_common(idx)
        diagnostics = diagnostics.filter(idx, value)
        print(f"After {idx+1} digits, there are {len(diagnostics)}")
        if len(diagnostics) == 1:
            break
    else:
        raise ValueError("Oops, ran off the end")

    oxygen = diagnostics.codes[0]

    # reset
    diagnostics.codes = codes
    # Get the oxygen value
    for idx in range(diagnostics.code_size):
        value = diagnostics.least_common(idx)
        diagnostics = diagnostics.filter(idx, value)
        print(f"After {idx+1} digits, there are {len(diagnostics)}")
        if len(diagnostics) == 1:
            break
    else:
        raise ValueError("Oops, ran off the end")

    co2 = diagnostics.codes[0]

    return oxygen, co2


if __name__ == "__main__":
    sys.exit(main())
