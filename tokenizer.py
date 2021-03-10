from token import Token, TokenTypes
from logger import Logger, LogTypes


class Tokenizer:
    VALID_CHARACTERS: [str] = ["1", "2", "3", "4",
                               "5", "6", "7", "8", "9", "0", "+", "-"]
    origin: str
    position: int
    actual: Token
    logger: Logger

    def __init__(self, code: str, logger: Logger):
        self.origin = code
        self.position = -1
        self.actual = None
        self.logger = logger

    def selectNext(self):
        self.position += 1

        if not self.isPositionValid(self.position):
            self.actual = Token(None, TokenTypes.EOF)
            return

        c = self.origin[self.position]

        while c not in self.VALID_CHARACTERS:
            self.position += 1

            if c not in self.VALID_CHARACTERS and c != " ":
                self.logger.log(LogTypes.ERROR, f"Unknown character '{c}'")
            elif not self.isPositionValid(self.position):
                self.actual = Token(None, TokenTypes.EOF)
                return
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
            self.logger.log(LogTypes.ERROR, f"Unknown character '{c}'")

    def isPositionValid(self, position: int):
        return position < len(self.origin)
