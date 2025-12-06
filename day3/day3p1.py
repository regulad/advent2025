#!/usr/bin/env python3

from itertools import combinations

if __name__ == "__main__":
    total_joltage_accum = 0
    with open("./input", "tr") as input_fp:
        for line in input_fp.readlines():
            bank_str = line.strip()
            # unimplemented optmization: generating combinations after a max has been found is unneccesary
            # however i think combinations is faster than writing a python loop that implements that logic
            # surely concatination is slow
            total_joltage_accum += max(map(lambda combination: int(combination[0] + combination[1]), combinations(bank_str, 2)))
    print(total_joltage_accum)
