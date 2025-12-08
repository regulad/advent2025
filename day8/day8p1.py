#!/usr/bin/env python3

from collections import deque
from functools import reduce
from math import prod, sqrt
from typing import Iterable, Iterator

from scipy.spatial import KDTree
import numpy as np

KDTREE_SEARCH_ITERATION_STEP: float = 0.5
NUM_CONNECTIONS_TO_MAKE = 1000

if __name__ == "__main__":
    # probably a better way to search for this with a dict or set but it gets messy
    circuits: list[frozenset[tuple[int, int, int]]] = []
    with open("./input", "tr") as input_fp:
        # have to use an array of tuples because tuples are hashable. numpy and scipy should be able to flatten them
        # would have preferred to use a set but ordering is important for the scipy KDTree; it only returns indexes and not nodes with .query
        breakers = tuple(
            tuple(int(p) for p in line.strip().split(","))
            for line in input_fp
            if line.strip()
        )
    # initialize circuits with one-breaker circuits
    for breaker in breakers:
        circuits.append(frozenset({breaker}))
    breaker_tree = KDTree(breakers)

    long_dist = 1
    already_processed_pairs: set[tuple[int, int]] = set()
    i = 0
    while i < NUM_CONNECTIONS_TO_MAKE:
        print(f"trying connection {i + 1}")  # TODO: DEBUG
        # a KDTree does not directly allow for efficent querying of the pair of items that are closest together,
        # however it DOES allow for the efficient querying of a pair of elements that are r apart
        # i use KDTREE_SEARCH_ITERATION_STEP to gradually "fan out" in order to find the closes two together
        # the dataset is something like a "3d golomb ruler" where each pair is guaranteed to have a unique distance
        breaker1: tuple[int, int, int] = None
        breaker2: tuple[int, int, int] = None
        
        substep = KDTREE_SEARCH_ITERATION_STEP
        while True:
            # maybe a more memory-efficient way to do this juggling
            all_pairs = frozenset(breaker_tree.query_pairs(long_dist, output_type="set"))
            new_pairs = all_pairs - already_processed_pairs

            pair_to_process: tuple[int, int] | None = None
            match len(new_pairs):
                case 0:
                    long_dist += substep
                    continue
                case 1:
                    # NOTE: np.uint64 's do not behave correctly in sets. no idea why, maybe broken hash?
                    pair_to_process = next(iter(new_pairs))  # no pop on a frozenset
                    breaker1 = breakers[pair_to_process[0]]
                    breaker2 = breakers[pair_to_process[1]]
                    already_processed_pairs |= new_pairs
                    break
                case _:
                    # print(f"got more than one at once at {long_dist-substep}+{substep}, refining search...")  # TODO: DEBUG
                    long_dist -= substep
                    substep /= 2
                    continue
        
        # we now have a pair of candidates!
        circuit1: frozenset[tuple[int, int, int]] | None = None
        circuit2: frozenset[tuple[int, int, int]] | None = None
        # need to do a linear search to find circuit1 and circuit2. 
        # i tried to do it with a dict but the side effects were difficult to trace
        for circuit in circuits:
            if breaker1 in circuit:
                circuit1 = circuit
            if breaker2 in circuit:
                circuit2 = circuit
            if circuit1 is not None and circuit2 is not None:
                break

        if circuit1 == circuit2:
            # already in the same circuit. need to retry.
            # print("already in the same circuit, moving on!")  # TODO: DEBUG
            # NOTE: ok, this one escaped me for a long while. the prompt expects you to count these cases where nothing happens as a "link", but the wording is ambiguous about what happens in those cases
            i += 1  # MUST increment here
            continue

        new_circuit = circuit1 | circuit2
        circuits.remove(circuit1)
        circuits.remove(circuit2)
        circuits.append(new_circuit)
        # would be better with j pointers but python is iffy
        i += 1  # a connection has been made between two circuits; go on
    unique_circuits = frozenset(circuits)
    unique_circuits_lens = sorted((len(unique_circuit) for unique_circuit in unique_circuits), reverse=True)
    print(unique_circuits_lens)
    print(f"check {prod(unique_circuits_lens[:3])} across {len(unique_circuits)} circuits")

