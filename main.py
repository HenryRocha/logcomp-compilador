import argparse
import pathlib
import sys
from parser import Parser

from logger import logger


def main() -> None:
    # Argparse, to enalbe the debug flag.
    parser = argparse.ArgumentParser()
    parser.add_argument(dest="sourceFile", type=str, help="source code")
    parser.add_argument("-d", "--debug", action="store_true", help="run in debug mode", default=False)
    parser.add_argument("-v", "--verbosity", action="count", help="verbosity level", default=0, required=False)
    args = parser.parse_args()

    sourceFile = pathlib.Path(args.sourceFile)
    logger.configure(enable=bool(args.debug), verbosity=int(args.verbosity))

    if not sourceFile.exists() or not sourceFile.is_file():
        logger.critical(f"[Main] No file named '{args.sourceFile}'")
    else:
        logger.info("[Main] Reading source file...")
        with open(sourceFile.absolute(), "r") as f:
            sourceCode = f.read()
        logger.info("[Main] Done")

    # Parse and calculate the result.
    Parser().run(sourceCode)


if __name__ == "__main__":
    main()
