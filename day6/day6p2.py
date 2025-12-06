#!/usr/bin/env python3

from io import StringIO, SEEK_END, SEEK_CUR
from math import prod  # don't need to do our own reduce

if __name__ == "__main__":
    with StringIO(newline="") as operand1fp, \
            StringIO(newline="") as operand2fp, \
            StringIO(newline="") as operand3fp, \
            StringIO(newline="") as operand4fp, \
            StringIO(newline="") as operatorfp:
        # I was going to have each of the StringIO fps 
        # be a reader at a different offset in the input_fp
        # to leverage the page cache, but that would require
        # me reading to the end of each line to get the location
        # of the newline anyway. This is just easier.
        with open("./input", "tr") as input_fp:
            # useful to know: all lines are the same length
            operand1fp.write(input_fp.readline().rstrip("\n"))
            operand2fp.write(input_fp.readline().rstrip("\n"))
            operand3fp.write(input_fp.readline().rstrip("\n"))
            operand4fp.write(input_fp.readline().rstrip("\n"))
            operatorfp.write(input_fp.readline().rstrip("\n"))
        # to ensure last line processes correctly
        operand1fp.write(" ")
        operand2fp.write(" ")
        operand3fp.write(" ")
        operand4fp.write(" ")
        operatorfp.write(" ")

        # reset
        operand1fp.seek(0)
        operand2fp.seek(0)
        operand3fp.seek(0)
        operand4fp.seek(0)
        operatorfp.seek(0)

        # parsing done, time to process
        accumulator = 0
        last_operator = operatorfp.read(1)
        while last_operator:
            with StringIO(
                    initial_value=last_operator,
                    newline=""
                ) as operator_buffer:
                operator_buffer.seek(0, SEEK_END)
                while True:
                    next_char = operatorfp.read(1)
                    if next_char == " ":
                        operator_buffer.write(next_char)
                    else:
                        last_operator = next_char
                        break
                operator_string = operator_buffer.getvalue()
            
            length_of_operator = len(operator_string)
            operator = operator_string[0]
            
            operands = []

            # convert to vertical strings piecewise; do len - 1 to exclude delimiting whitespace and seek 1 after SEEK_CUR
            for _ in range(length_of_operator - 1):
                with StringIO(newline="") as this_operand_fp:
                    this_operand_fp.write(operand1fp.read(1))
                    this_operand_fp.write(operand2fp.read(1))
                    this_operand_fp.write(operand3fp.read(1))
                    this_operand_fp.write(operand4fp.read(1))
                    # done
                    operands.append(int(this_operand_fp.getvalue().strip()))
            # SEEK_CUR doesn't actually work on strings! because UTF-16 support; just read a char instead
            operand1fp.read(1)  # operand1fp.seek(1, SEEK_CUR)
            operand2fp.read(1)  # operand2fp.seek(1, SEEK_CUR)
            operand3fp.read(1)  # operand3fp.seek(1, SEEK_CUR)
            operand4fp.read(1)  # operand4fp.seek(1, SEEK_CUR)

            match operator:
                case "+":
                    accumulator += sum(operands)
                case "*":
                    accumulator += prod(operands)
        print(accumulator)

