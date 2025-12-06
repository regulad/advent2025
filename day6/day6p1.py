#!/usr/bin/env python3

from io import StringIO, SEEK_END

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
            operand1str = operand1fp.read(length_of_operator)
            operand2str = operand2fp.read(length_of_operator)
            operand3str = operand3fp.read(length_of_operator)
            operand4str = operand4fp.read(length_of_operator)

            operand1int = int(operand1str.rstrip(" "))
            operand2int = int(operand2str.rstrip(" "))
            operand3int = int(operand3str.rstrip(" "))
            operand4int = int(operand4str.rstrip(" "))

            match operator_string[0]:
                case "+":
                    accumulator += operand1int + operand2int + operand3int + operand4int
                case "*":
                    accumulator += operand1int * operand2int * operand3int * operand4int
        print(accumulator)

