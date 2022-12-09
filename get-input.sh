#!/bin/sh

curl "https://adventofcode.com/${1}/day/${2}/input" \
    --header "Cookie: $(cat .token)" \
    --output ${1}/day${2}-input.txt
