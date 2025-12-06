#!/usr/bin/env python3

if __name__ == "__main__":
    password_accum = 0
    dial_position = 50
    with open("input", "r") as seq_file:
        for instruction in seq_file.readlines():
            operation = instruction[0]
            operand = int(instruction[1:].strip()) # the number in the instruction

            if operation == "L":
                sign = -1
                if dial_position % 100 != 0 and dial_position % 100 < operand % 100:
                    password_accum += 1
            else:
                sign = 1
                if (dial_position % 100) + (operand % 100) > 100:
                    password_accum += 1
            
            dial_position += sign * operand
            password_accum += operand // 100 # cycles gone around
            if dial_position % 100 == 0:
                password_accum += 1
    print(password_accum)
