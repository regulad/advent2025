#!/usr/bin/env python3

import datetime
import time

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

                if id_to_test_str_len % 2 == 1:
                    # an id composed of 2 repeats cant have an odd length 
                    continue
                
                id_to_test_str_midway = id_to_test_str_len // 2
                if id_to_test_str[:id_to_test_str_midway] == id_to_test_str[id_to_test_str_midway:]:
                    invalid_id_accum += id_to_test

    time_end = time.perf_counter_ns()
    total_ns = time_end - time_begin
    elapsed_td = datetime.timedelta(microseconds=(total_ns // 1_000))
    print(f"got {invalid_id_accum} in {elapsed_td}")
