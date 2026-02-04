import sys
import fileinput
from Q2.part_b import main
from helpers import q2_input

if __name__ == "__main__":
    for arg in sys.argv[1:]:
        if arg == "1":
            print("Testing Q1")
        elif arg == "2":
            print("Testing Q2A")
            input = fileinput.input("tests/q2a_test1.in")
            g, s = q2_input(input)
            # Solve Q2A
            input.close()

            input = fileinput.input("tests/q2a_test2.in")
            g, s = q2_input(input)
            # Solve Q2A
            input.close()
        elif arg == "3":
            print("Testing Q2B")
            input = fileinput.input("tests/q2b_test.in")
            g, s = q2_input(input)
            main(g, s)
            input.close()
        else:
            print("Please provide at least 1 argument of 1, 2, or 3.")