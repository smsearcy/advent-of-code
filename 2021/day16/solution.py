#!/usr/bin/env python3
"""Day 16: Packet Decoder

Given that it is using unconventional sizes (like 3 bit integers),
I don't think I can use Python's `struct` library.

Usage: ./solution.py 1|2 FILE

"""

from __future__ import annotations

import sys
import typing as t
from argparse import ArgumentParser
from dataclasses import dataclass

verbose = False


@dataclass
class Packet:
    version: int

    @classmethod
    def parse(cls, message: str) -> tuple[Packet, str]:
        if message[3:6] == "100":
            return Value.parse(message)
        else:
            return Operator.parse(message)


@dataclass
class Value(Packet):
    value: int

    @classmethod
    def parse(cls, message: str) -> tuple[Value, str]:
        version = int(message[:3], 2)
        offset = 6
        done = False
        value_bits = ""
        while not done:
            chunk = message[offset : offset + 5]
            if chunk[0] == "0":
                done = True
            value_bits += chunk[1:]
            offset += 5

        return Value(version=version, value=int(value_bits, 2)), message[offset:]


@dataclass
class Operator(Packet):
    type: int
    sub_packets: list[Packet]

    @classmethod
    def parse(cls, message: str) -> tuple[Operator, str]:
        version = int(message[:3], 2)
        type_ = int(message[3:6], 2)
        length_type = message[6:7]
        if length_type == "0":
            bit_length = int(message[7:22], 2)
            packets, remainder = parse_bit_length_packets(message[22:], bit_length)
        else:
            packet_count = int(message[7:18], 2)
            packets, remainder = parse_count_packets(message[18:], packet_count)
        return Operator(version=version, type=type_, sub_packets=packets), remainder


def parse_bit_length_packets(message: str, length: int) -> tuple[list[Packet], str]:
    pass


def parse_count_packets(message: str, count: int) -> list[Packet]:
    pass


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
    transmissions = read_file(filename)
    for transmission in transmissions:
        message = f"{int(transmission, 16):b}"
        if verbose:
            print("Message:", message)
        packets = Packet.parse(message)
        if verbose:
            print("Packets:", packets)


def part2(filename):
    pass


def read_file(filename) -> list[str]:
    with open(filename, "r") as f:
        transmissions = [line.strip() for line in f]
    return transmissions


def parse_bits(message: str) -> tuple[Packet, str]:
    """Parse a Buoyancy Interchange Transmission System message."""


if __name__ == "__main__":
    sys.exit(main())
