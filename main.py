import sys
from parser import Parser


if __name__ == "__main__":
    VALID_CHARACTERS = ["1", "2", "3", "4",
                        "5", "6", "7", "8", "9", "0", "+", "-", " "]

    # Get the first argument and parse it as a string.
    originalMath = str(sys.argv[1]).strip()

    # Check for:
    # ""
    if len(originalMath) == 0:
        raise ValueError("Empty input.")

    # Check for:
    # Any characters not supported.
    if not set(originalMath).issubset(VALID_CHARACTERS):
        raise ValueError("Input contains invalid characters.")

    # Check for:
    # "+" / "-" / "+1" / "1-"
    if not originalMath[0].isdigit() or not originalMath[-1].isdigit():
        raise ValueError("Starting or ending character in not a digit.")

    # Parse and calculate.
    print(Parser().run(originalMath))
