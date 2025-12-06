#!/usr/bin/env python3

if __name__ == "__main__":
    password_accum = 0
    dial_position = 50
    with open("input", "r") as seq_file:
        for instruction in seq_file.readlines():
            operation = instruction[0]
            operand = int(instruction[1:]) # the number in the instruction
            sign: int
            match operation:
                case "L":
                    sign = -1
                case "R":
                    sign = 1
                case _:
                    raise RuntimeError("Bad instruction")
            
            dial_position += sign * operand
            if dial_position % 100 == 0:
                password_accum += 1
    print(password_accum)
