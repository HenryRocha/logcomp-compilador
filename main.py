import sys
import argparse
from parser import Parser
from logger import Logger


def main() -> None:
    # Argparse, to enalbe the debug flag.
    parser = argparse.ArgumentParser()
    parser.add_argument(dest="sourceFile", type=str, help="source code")
    parser.add_argument("-d", "--debug", action="store_true", help="run in debug mode", default=False)
    args = parser.parse_args()

    try:
        with open(str(args.sourceFile).strip(), "r") as f:
            sourceCode = f.read()
    except:
        raise ValueError(f"No file named '{args.sourceFile}'")

    # Parse and calculate the result.
    Parser(Logger(args.debug)).run(sourceCode)


if __name__ == "__main__":
    main()
