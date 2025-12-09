#!/usr/bin/env python3

from itertools import combinations

def rectangle_size(coord1: tuple[int, int], coord2: tuple[int, int]) -> int:
    """
    Gets the size of a rectangle drawn between two points on a 2d plane.
    """
    # Only broken out to a function because its a little too long to write in a lambda
    return (abs(coord2[0] - coord1[0]) + 1) * (abs(coord2[1] - coord1[1]) + 1)

if __name__ == "__main__":
    # For part one, the real dataset is only 500 coordinates large.
    # 500 choose 2 is small enough that brute forcing it is trivial.
    # Plus, I haven't any idea how to do it without brute forcing. Oops.
    pairs: set[tuple[int, int]] = set()
    with open("./input", "tr") as input_fp:
        for line in input_fp.readlines():
            # I learned today that canonically AoC inputs do NOT end with a line break.
            # So, technically, the following clause is pointless. 
            # Still I think nano and vi often insert \n at the end of a file when saving if it's been edited.
            if not line:
                break
            pair = tuple(int(coord) for coord in line.strip().split(","))
            pairs.add(pair)
    max_seen = max(rectangle_size(coord1, coord2) for coord1, coord2 in combinations(pairs, 2))
    print(max_seen)

