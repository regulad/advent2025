#!/usr/bin/env python3

if __name__ == "__main__":
    ranges: list[tuple[int, int]] = []
    ids: list[int] = []
    accum_fresh = 0

    with open("./input", "tr") as input_fp:
        lines_iterator = iter(input_fp.readlines())

        while True:
            current_range = next(lines_iterator).strip()
            if not current_range:
                break
            ranges.append(
                tuple(
                    [
                        int(bound)
                        for bound
                        in current_range.split("-")
                    ]
                )
            )

        # try:
        #     while True:
        #         current_id = next(lines_iterator).strip()
        #         ids.append(
        #             int(current_id)
        #         )
        # except StopIteration:
        #     pass

    # second step: just count
    last_upper_bound = 0
    for lower_bound, upper_bound in sorted(ranges, key=lambda r: r[0]):
        print(lower_bound, upper_bound)
        if last_upper_bound >= lower_bound:
            print("overlap!")
            if upper_bound == lower_bound \
                    or upper_bound <= last_upper_bound:
                continue
            lower_bound = last_upper_bound + 1
        assert upper_bound >= lower_bound
        accum_fresh += upper_bound - lower_bound + 1
        last_upper_bound = upper_bound

    print(accum_fresh)

