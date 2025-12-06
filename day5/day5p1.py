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

        try:
            while True:
                current_id = next(lines_iterator).strip()
                ids.append(
                    int(current_id)
                )
        except StopIteration:
            pass

    for food_id in ids:
        for lower_bound, upper_bound in ranges:
            if lower_bound <= food_id and food_id <= upper_bound:
                accum_fresh += 1
                break

    print(accum_fresh)
