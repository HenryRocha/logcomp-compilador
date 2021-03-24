import sys
import argparse
from parser import Parser
from logger import Logger


def main() -> None:
    # Default variables.
    debug = False
    originalMath = ""

    if len(sys.argv) == 1:
        raise ValueError(f"No arguments given")
    elif len(sys.argv) == 2:
        originalMath = sys.argv[1]
    elif len(sys.argv) == 3:
        if sys.argv[1] == "-d":
            debug = True
        if sys.argv[2] != "" and sys.argv[2] != "-d":
            originalMath = sys.argv[2]
        else:
            raise ValueError("Bad arguments")

    # Parse and calculate the result.
    result = Parser(Logger(debug)).run(originalMath)
    print(result)


if __name__ == "__main__":
    main()
