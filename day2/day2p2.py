#!/usr/bin/env python3

import datetime
import functools
import time

from sympy import factorint

@functools.cache # many ids will have the same len; this saves worthless recalculation
def get_all_possible_substring_len(full_str_len: int) -> set[int]:
    possible_substring_lens = set()

    for factor, appearances in factorint(full_str_len).items():
        for power in range(0, appearances + 1):
            possible_substring_lens.add(factor ** power)

    # not safe, but doesn't matter
    return possible_substring_lens

if __name__ == "__main__":
    time_begin = time.perf_counter_ns()
    invalid_id_accum = 0

    with open("./input", "tr") as input_file:
        raw_ids_line = input_file.readline()
        for id_range in raw_ids_line.split(","):
            id_range_lower_str, id_range_upper_str = id_range.split("-")
            # temporary brute force solution
            id_range_lower_int = int(id_range_lower_str)
            id_range_upper_int = int(id_range_upper_str)
            for id_to_test in range(id_range_lower_int, id_range_upper_int + 1, 1):
                # don't have to test for leading 0's
                id_to_test_str = str(id_to_test)
                id_to_test_str_len = len(id_to_test_str)

                # any possible repeat substring length is a factor of its length
                for possible_substring_len in get_all_possible_substring_len(id_to_test_str_len):
                    if possible_substring_len == id_to_test_str_len:
                        continue
                    num_slices = id_to_test_str_len // possible_substring_len  # guaranteed to be > 1 when possible_substring_len != id_to_test_str_len
                    slice_one = id_to_test_str[:possible_substring_len]
                    for i in range(1, num_slices):
                        this_slice = id_to_test_str[i*possible_substring_len:(i+1)*possible_substring_len]
                        # print(f"{id_to_test_str}: {slice_one} vs {this_slice}")  # DEBUG
                        if this_slice != slice_one:
                            break
                    else:
                        invalid_id_accum += id_to_test
                        break

    time_end = time.perf_counter_ns()
    total_ns = time_end - time_begin
    elapsed_td = datetime.timedelta(microseconds=(total_ns // 1_000))
    print(f"got {invalid_id_accum} in {elapsed_td}")
