#!/usr/bin/env python3

from datetime import timedelta
from functools import reduce
from time import perf_counter_ns
from typing import Literal

type BaleType = Literal["."] | Literal["x"] | Literal["@"] | Literal["!"]
type BaleRowType = list[BaleType]
type BaleArrayType = list[BaleRowType]

def pretty_perf(before_ns: int, /) -> str:
    """Returns a pretty rendition of the time between a previous point in time and now."""
    now_ns = perf_counter_ns()
    difference_ns = now_ns - before_ns
    difference_td = timedelta(microseconds=(difference_ns // 1_000))
    return str(difference_td)

def pretty_array(bale_array: BaleArrayType, /) -> str:
    """Returns a pretty string redition of a bale array."""
    return "\n".join(
        [
            reduce(
                lambda accum, nexti: accum + nexti, 
                bale_row,
                ""
            )
            for bale_row
            in bale_array
        ]
    )

if __name__ == "__main__":
    # While my previous solutions have relied on "lazy" line-wise loading, I'm going to preload this so I can perform
    # my image-processing kernel style processing.
    # Maybe if I get really bored, I'll vectorize this application and offload it to GPU. But I won't get that bored, sorry.
    working_array: BaleArrayType = []

    preload = perf_counter_ns()
    with open("./input", "tr") as input_fp:
        for bale_row_raw in input_fp.readlines():
            bale_row = bale_row_raw.strip()
            if not bale_row:
                break
            vector_to_insert: BaleRowType = []
            for bale_char in bale_row:
                vector_to_insert.append(bale_char)
            working_array.append(vector_to_insert)
    width = len(working_array[0])
    height = len(working_array)
    assert reduce(lambda compliant, vector: (compliant and len(vector) == width), working_array, True)  # find if vectors in matrix are a homogenous width since we aren't using numpy
    assert width == height
    print(f"Loaded a {width}x{height} matrix in {pretty_perf(preload)}")
    print()
    del preload

    print(pretty_array(working_array))
    print()

    # while true here is a stub for part 2 of this problem
    preprocess = perf_counter_ns()
    cycles = 0
    while True:
        cycles += 1
        did_modify_this_loop = False
        for h in range(height):
            for w in range(width):
                bale = working_array[h][w]
                if bale != "@":
                    continue
                # need to do math to see if this bale can be removed, and if so, remove it
                accum_neighbours = 0
                # this is essentially an extremely primitive convolutional kernel
                for hr, wr in (
                            (-1, -1), (-1, 0), (-1, 1),
                            (0, -1),           (0, 1),
                            (1, -1),  (1, 0),  (1, 1),
                        ):
                    # first check to see if we're in bounds
                    hra = h + hr
                    wra = w + wr
                    if hra >= 0 and hra < height \
                            and wra >= 0 and wra < width \
                            and (working_array[hra][wra] == "@" 
                                 or working_array[hra][wra] == "!"):
                        accum_neighbours += 1
                if accum_neighbours < 4:
                    working_array[h][w] = "!"
                    did_modify_this_loop = True
        # collapse temp marker ! into x
        for h in range(height):
            for w in range(width):
                if working_array[h][w] == "!":
                    working_array[h][w] = "x"
        print(pretty_array(working_array))
        print()
        if not did_modify_this_loop:
            break
    
    bales_removed = reduce(
        lambda accum, row_accum: accum + row_accum,
        [
            reduce(
                lambda accum, bale: accum + 1 if bale == "x" else accum,
                bale_row,
                0
            )
            for bale_row
            in working_array
        ],
        0
    )
    print(f"Removed {bales_removed} across {cycles} iterations in {pretty_perf(preprocess)}")
    del preprocess

