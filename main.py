import sys


if __name__ == "__main__":
    VALID_CHARACTERS = ["1", "2", "3", "4",
                        "5", "6", "7", "8", "9", "0", "+", "-", " "]
    VALID_OPERATORS = ["+", "-"]

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

    # Holds all the valid numbers.
    operands = []
    # Holds all the valid operators.
    operators = []

    # Helper to build the number from individual characters.
    numberBuilder = ""
    # Helper to indicate if the last character was a digit.
    previousIsDigit = False

    # Loop through all characters
    for i, char in enumerate(originalMath):
        if char.isdigit():
            # If it is a digit, add it to the current number.
            numberBuilder += char

            # If the last character is a digit, we need to append the current
            # number to the list now, instead of waiting for the next not digit
            # character.
            if i == len(originalMath) - 1:
                operands.append(int(numberBuilder))

            # Indicate that this character is a digit.
            previousIsDigit = True
        else:
            # In case the last character was a digit we add it to the list and
            # reset the helper variables.
            if previousIsDigit:
                operands.append(int(numberBuilder))
                numberBuilder = ""

            if char in VALID_OPERATORS:
                operators.append(char)
            elif char == " " and previousIsDigit:
                # In case there is a whitespace after a digit, go throught the
                # list looking for a valid operator.
                valid = True
                for k, char in enumerate(originalMath[i:]):
                    if char == " ":
                        continue
                    elif char in VALID_OPERATORS:
                        break
                    else:
                        valid = False

                if not valid:
                    raise ValueError("Found empty space between digits.")

            # Indicate that this character is not a digit.
            previousIsDigit = False

    # Since the above loop does not check for duplicated operators,
    # we do this instead. The lenghts
    if len(operators) != len(operands) - 1:
        raise ValueError("Double '+' or '-' somewhere.")

    # Variable that holds the results, from left to right.
    # Which means the last value is the latest result.
    results = []

    # Go through all operators and do the math.
    for i, operator in enumerate(operators):
        if operator == "+":
            # If there is something in the results list, use it.
            if len(results) > 0:
                results.append(results[-1] + operands[i + 1])
            else:
                results.append(operands[i] + operands[i + 1])
        elif operator == "-":
            # If there is something in the results list, use it.
            if len(results) > 0:
                results.append(results[-1] - operands[i + 1])
            else:
                results.append(operands[i] - operands[i + 1])

    # Print the actual result.
    print(results[-1])
