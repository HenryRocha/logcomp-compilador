import sys
from parser import Parser


if __name__ == "__main__":
    # Get the first argument, parse it as a string and remove any traling whitespaces,
    # at the end or the beginning of the string.
    originalMath = str(sys.argv[1]).strip()

    # Parse and calculate the result.
    print(Parser().run(originalMath))
