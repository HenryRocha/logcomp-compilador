import sys
from parser import Parser


if __name__ == "__main__":
    VALID_CHARACTERS = ["1", "2", "3", "4",
                        "5", "6", "7", "8", "9", "0", "+", "-", " "]

    # Get the first argument, parse it as a string and remove any traling whitespaces,
    # at the end or the beginning of the string.
    originalMath = str(sys.argv[1]).strip()

    # Parse and calculate the result.
    print(Parser().run(originalMath))
