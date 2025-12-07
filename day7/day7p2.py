#!/usr/bin/env python3

from copy import deepcopy
from functools import cache

# board characters: 
#    - S: tachyon beam source
#    - ^: beam splitter
#    - .: empty

# to enable state tracking, we add some more characters as we proceed line-by-line:
#    - |: active tachyon beam (created below tachyon beam sources, active tachyon beams, and excited beam splitters)
#    - !: excited beam splitter (created when a beam splitter is activated; will create two beams next to it)

# untracked in mutated board but still conceptually active
#    - f: "fork point;" an active tachyon beam that is sythetically accurate and not neccesarily accurate (like a superposition)
#        the timeline evaluation function splits here

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
     
    @cache
    def evaluate_board_timelines(starti: int = 0, beamloc: int | None = None) -> int:
        """
        Given a board that starts on row 0 (may be sliced from the greater board at row n,
        this function evaluates how many alternative timelines the board can diverge into.
        """
    
        # EITHER we reach the end of the board (0 timelines left) or there is a splitter to be encountered
        for i in range(starti + 1, len(board)):
            this_row = board[i]
    
            if beamloc is None:
                # easier to ask for forgiveness than to ask for permission; 
                # is python's try except handling faster than "#__contains__" + "index"? not sure but will assume it is       
                previous_row = board[i-1]
                try:
                    beamloc = previous_row.index("|")
                    assert previous_row.count("|") == 1
                except ValueError:
                    beamloc = previous_row.index("S")
                    assert previous_row.count("S") == 1
    
            # if the char at the current beamloc is "|", we just continue to the next cycle since the beamloc doesn't change        
            if this_row[beamloc] == "^":
                # originally, i wanted to use slicing here.
                # however, slicing turns out to be crazily slow and makes up the majority of each cycle once it gets going fast enough
                # starti is used as the starting pos instead of slicing to start at i and passing that as the board
                return evaluate_board_timelines(i, beamloc - 1) + evaluate_board_timelines(i, beamloc + 1) 
        else:
            return 1

    print(evaluate_board_timelines())

