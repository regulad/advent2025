#!/usr/bin/env python3

from io import StringIO, SEEK_END
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
            # each of these strings is a char longer than it needs to be but we never seek that far
            operand1str = operand1fp.read(length_of_operator)
            operand2str = operand2fp.read(length_of_operator)
            operand3str = operand3fp.read(length_of_operator)
            operand4str = operand4fp.read(length_of_operator)
            
            operands = []

            # convert to vertical strings piecewise
            with StringIO(operand1str, newline="") as hoperand1fp, \
                    StringIO(operand2str, newline="") as hoperand2fp, \
                    StringIO(operand3str, newline="") as hoperand3fp, \
                    StringIO(operand4str, newline="") as hoperand4fp:
                for _ in range(length_of_operator - 1):
                    with StringIO(newline="") as this_operand_fp:
                        this_operand_fp.write(hoperand1fp.read(1))
                        this_operand_fp.write(hoperand2fp.read(1))
                        this_operand_fp.write(hoperand3fp.read(1))
                        this_operand_fp.write(hoperand4fp.read(1))
                        # done
                        operands.append(int(this_operand_fp.getvalue().strip()))
            
            match operator:
                case "+":
                    accumulator += sum(operands)
                case "*":
                    accumulator += prod(operands)
        print(accumulator)

