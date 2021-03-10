from token import Token
from token_types import TokenTypes


class Tokenizer:
    VALID_CHARACTERS: [str] = ["1", "2", "3", "4",
                               "5", "6", "7", "8", "9", "0", "+", "-"]
    origin: str
    position: int
    actual: Token

    def __init__(self, code: str):
        self.origin = code
        self.position = -1
        self.actual = None

    def selectNext(self):
        self.position += 1

        if not self.isPositionValid(self.position):
            self.actual = Token(None, TokenTypes.EOF)
            return

        c = self.origin[self.position]

        while c not in self.VALID_CHARACTERS:
            self.position += 1

            if not self.isPositionValid(self.position):
                self.actual = Token(None, TokenTypes.EOF)
                return
            elif c not in self.VALID_CHARACTERS and c != " ":
                raise ValueError(f"Unknown character '{c}'")
            else:
                c = self.origin[self.position]

        if c == "+":
            self.actual = Token(c, TokenTypes.PLUS)
        elif c == "-":
            self.actual = Token(c, TokenTypes.MINUS)
        elif c.isdigit():
            numberBuilder = [char if char.isdigit(
            ) else "X" for char in self.origin[self.position:]]
            numberBuilder = "".join(numberBuilder).split("X")[0]

            self.position += len(numberBuilder) - 1
            self.actual = Token(numberBuilder, TokenTypes.NUMBER)
        else:
            raise ValueError("Uknown character found.")

    def isPositionValid(self, position: int):
        return position < len(self.origin)
