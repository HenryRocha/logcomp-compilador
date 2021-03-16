import sys
import argparse
from parser import Parser
from logger import Logger


if __name__ == "__main__":
    # Argparse, to enalbe the debug flag.
    parser = argparse.ArgumentParser()
    parser.add_argument(dest="originalMath", type=str, help="Math to be evaluated")
    parser.add_argument("-d", "--debug", action="store_true", help="run in debug mode", default=False)
    args = parser.parse_args()

    # Get the first argument, parse it as a string and remove any traling whitespaces,
    # at the end or the beginning of the string.
    originalMath = str(args.originalMath).strip()

    # Parse and calculate the result.
    result = Parser(Logger(args.debug)).run(originalMath)

    if args.debug:
        print(f"Result: {result}  ||  Eval result: {eval(originalMath)}")
    else:
        print(result)
