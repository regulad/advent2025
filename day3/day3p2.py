#!/usr/bin/env python3

from itertools import combinations, chain, repeat, filterfalse

if __name__ == "__main__":
    total_joltage_accum = 0
    with open("./input", "tr") as input_fp:
        for line in input_fp.readlines():
            bank_str = line.strip()
            # unimplemented optmization: generating combinations after a max has been found is unneccesary
            # however i think combinations is faster than writing a python loop that implements that logic
            # surely concatination is slow
            # part 2 addl. constraint: must test combination of lengths 1-n where each bank is length n
            # still O(n), though, each row just takes longer
            
            # >>> len(list(combinations("811111111111119", 2)))
            # 105
            # >>> len(list(combinations("811111111111119", 12)))
            # 455
            # and a "prod" bank is 100 chars... -> brute forcing part 2 will take 676 years

            # # brute force impl of part 2: too slow + i have an idea for an efficient impl
            # total_joltage_accum += max(
            #     map(
            #         lambda combination: int("".join(combination)), 
            #         combinations(bank_str, 12)
            #     )
            # )

            # "smart" impl of part 2
            bank_str_len = len(bank_str)
            bank_int_array = tuple(map(int, bank_str))  # read-only seq is fine but we access it randomly
            bank_take_keys = list(repeat(False, bank_str_len))  # need r/w array
            flattened_enumerate = tuple(enumerate(bank_int_array))  # faster to pre-iterate than fetch a ton of times

            # setup bank_take_keys
            accept_less = 0
            while bank_take_keys.count(True) < 12:
                assert accept_less >= 0 and accept_less < 9

                # if accept_less > 0, we are on a "pad" cycle to get us up to 12 digits rather than a cycle where we are trying to max out the number of digits
                # if we got a first one on the end, we still need to go from the top
                first_taken_index = bank_take_keys.index(True) if True in bank_take_keys else -1
                tailed_by_takes = all(bank_take_keys[first_taken_index:])
                for k in range(bank_str_len - 1, 0, -1):
                    eff_end_of_array_index = k
                    if not bank_take_keys[k]:
                        break

                if accept_less > 0 and first_taken_index < bank_str_len - 12:
                    this_cycle_iterator = reversed(flattened_enumerate)
                else:
                    this_cycle_iterator = flattened_enumerate

                if this_cycle_iterator != None:
                    for i, battery in filterfalse(lambda enumitem: bank_take_keys[enumitem[0]], this_cycle_iterator):
                        items_above = bank_int_array[i + 1:eff_end_of_array_index + 1]
                        if (not items_above or battery + accept_less >= max(items_above)) \
                                and (i > first_taken_index or tailed_by_takes):
                            bank_take_keys[i] = True
                            break
                    else:
                        # print("next cycle will accept less!")
                        accept_less += 1

                # print(bank_str)  # DEBUG
                # print("".join(map(lambda x: "x" if x else "-", bank_take_keys)))  # DEBUG

            # post-process
            bank_taken_ordered = map(
                lambda kv: str(kv[1]), 
                filter(
                     lambda enumitem: bank_take_keys[enumitem[0]],
                     enumerate(bank_str)
                )
            )
            largest_joltage_str = "".join(bank_taken_ordered)
            assert len(largest_joltage_str) == 12
            largest_joltage_int = int(largest_joltage_str)
            total_joltage_accum += largest_joltage_int
            
            # print()
    print(total_joltage_accum)
