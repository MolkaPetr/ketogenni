#!/usr/bin/env python3
"""Simple command-line calculator supporting basic arithmetic operations."""
import operator
import sys


def main() -> None:
    """Run the calculator based on command-line arguments."""
    if len(sys.argv) != 4:
        print("Usage: calculator.py <number> <operator> <number>")
        print("Operators: + - * /")
        sys.exit(1)
    try:
        left = float(sys.argv[1])
        right = float(sys.argv[3])
    except ValueError:
        print("Numbers must be numeric.")
        sys.exit(1)

    op = sys.argv[2]
    ops = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}
    if op not in ops:
        print("Invalid operator. Choose from + - * /.")
        sys.exit(1)
    if op == "/" and right == 0:
        print("Error: Division by zero.")
        sys.exit(1)

    result = ops[op](left, right)
    # Display as int if no fractional part
    print(int(result) if result.is_integer() else result)


if __name__ == "__main__":
    main()
