#! /usr/bin/python3

from math import factorial
from functools import reduce
from operator import mul
from os import get_terminal_size
from typing import Optional
from fractions import Fraction
import argparse

def choose(n: int, k: int) -> int:
    assert n >= k >= 0
    return reduce(mul, range(n-k+1, n+1), 1) // factorial(k)

def print_hist(n:int, p: Fraction, term_width: Optional[int] = None) -> None:
    possibilities = []
    ratios = []
    for i in range(0, n+1):
        bc = choose(n, i)
        ratio = bc * (p**i * (1-p)**(n-i))
        possibilities.append(bc)
        ratios.append(ratio)
    max_possibilities = possibilities[n//2]
    max_ratio = max(ratios)
    wi = len(str(n))
    wn = len(str(max_possibilities))
    if term_width is None:
        try:
            term_width = get_terminal_size().columns
        except OSError:
            term_width = 100
    hist_width = term_width - 27 - wi - wn
    accum_p = Fraction(0)
    for i, (bc, ratio) in enumerate(zip(possibilities, ratios)):
        accum_p += ratio
        print(f"{i:{wi}}: {bc:{wn}} {float(ratio):7.2%} {float(accum_p):7.2%} {float(1-accum_p):7.2%} " + '━' * round(hist_width * ratio/max_ratio))


def main(args: list[str]) -> int:
    parser = argparse.ArgumentParser(args[0])
    parser.add_argument('-n', type=int)
    parser.add_argument('-p', type=Fraction, default=Fraction(1,2))
    parser.add_argument('-w', type=int, default=None)
    parsed = parser.parse_args()
    p = parsed.p
    if not 0 <= p <= 1:
        print(f"Error: p musst be between 0 and 1")
        return 1
    print_hist(parsed.n, Fraction(p), term_width=parsed.w)
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))