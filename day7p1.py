#!/usr/bin/env python3

# board characters: 
#    - S: tachyon beam source
#    - ^: beam splitter
#    - .: empty

# to enable state tracking, we add some more characters as we proceed line-by-line:
#    - |: active tachyon beam (created below tachyon beam sources, active tachyon beams, and excited beam splitters)
#    - !: excited beam splitter (created when a beam splitter is activated; will create two beams next to it)

if __name__ == "__main__":
    board: list[list[str]] = []
    with open("./input", "tr") as input_fp:
        for line in input_fp.readlines():
            if not line:
                break
            this_row_chars: list[str] = []
            # very possibly a more efficient way to do this
            for space in line.rstrip("\n"):
                assert space == "S" or space == "^" or space == "."
                this_row_chars.append(space)
            board.append(this_row_chars)
     
    split_accum = 0
    for i in range(1, len(board)):
        previous_row = board[i-1]
        this_row = board[i]
        width = len(this_row)
        assert previous_row and this_row and width == len(previous_row)
        for k in range(width):
            char = this_row[k]  
            # if we want to use enumerate, we
            # have to create a copy since we cant iterate over a list we are changing(?)
            # so we just use naive indexing
            assert char == "." or char == "^"
            # the input board has empty rows inbetween every row with data; we can only worry about "diagonal" throws from excited splitters
            match char:
                case ".":
                    # handle right e. splitter, handle left e. splitter
                    # handle below S or |
                    if (k < width - 1 and previous_row[k + 1] == "!") \
                            or (k > 0 and previous_row[k - 1] == "!") \
                            or (previous_row[k] == "|" or previous_row[k] == "S"):
                        this_row[k] = "|"
                case "^":
                    if previous_row[k] == "|":
                        split_accum += 1
                        this_row[k] = "!"
        print("".join(this_row))
    print(split_accum)

