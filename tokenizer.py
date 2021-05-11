from tokens import Token, TokenTypes
from logger import Logger, LogTypes


class Tokenizer:
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

        while c == " " or c == "\n":
            self.position += 1

            if not self.isPositionValid(self.position):
                self.actual = Token(None, TokenTypes.EOF)
                return
            else:
                c = self.origin[self.position]

        if c == "+":
            self.actual = Token(c, TokenTypes.PLUS)

        elif c == "-":
            self.actual = Token(c, TokenTypes.MINUS)

        elif c == "*":
            self.actual = Token(c, TokenTypes.MULTIPLY)

        elif c == "/":
            self.actual = Token(c, TokenTypes.DIVIDE)

        elif c == "(":
            self.actual = Token(c, TokenTypes.LEFT_PARENTHESIS)

        elif c == ")":
            self.actual = Token(c, TokenTypes.RIGHT_PARENTHESIS)

        elif c == "=":
            if self.isPositionValid(self.position + 1) and self.origin[self.position + 1] == "=":
                self.position += 1
                self.actual = Token("==", TokenTypes.CMP_EQUAL)
            else:
                self.actual = Token(c, TokenTypes.ASSIGN)

        elif c == ">":
            self.actual = Token(c, TokenTypes.CMP_GREATER)

        elif c == "<":
            self.actual = Token(c, TokenTypes.CMP_LESS)

        elif c == "!":
            self.actual = Token(c, TokenTypes.NOT)

        elif c == "|":
            if self.isPositionValid(self.position + 1) and self.origin[self.position + 1] == "|":
                self.position += 1
                self.actual = Token("||", TokenTypes.CMP_OR)
            else:
                self.logger.log(LogTypes.ERROR, f"Comparison with only one '|' is not allowed")

        elif c == "&":
            if self.isPositionValid(self.position + 1) and self.origin[self.position + 1] == "&":
                self.position += 1
                self.actual = Token("&&", TokenTypes.CMP_AND)
            else:
                self.logger.log(LogTypes.ERROR, f"Comparison with only one '&' is not allowed")

        elif c == ";":
            self.actual = Token(c, TokenTypes.SEPARATOR)

        elif c == "{":
            self.actual = Token(c, TokenTypes.LEFT_BRACKET)

        elif c == "}":
            self.actual = Token(c, TokenTypes.RIGHT_BRACKET)

        elif c.isalpha():
            wordBuilder = [char if (char.isalnum() or char == "_") else "@" for char in self.origin[self.position :]]
            wordBuilder = "".join(wordBuilder).split("@")[0]
            self.position += len(wordBuilder) - 1

            if wordBuilder == "println":
                self.actual = Token(wordBuilder, TokenTypes.PRINT)
            elif wordBuilder == "readln":
                self.actual = Token(wordBuilder, TokenTypes.READLN)
            elif wordBuilder == "while":
                self.actual = Token(wordBuilder, TokenTypes.WHILE)
            elif wordBuilder == "if":
                self.actual = Token(wordBuilder, TokenTypes.IF)
            elif wordBuilder == "else":
                self.actual = Token(wordBuilder, TokenTypes.ELSE)
            else:
                self.actual = Token(wordBuilder, TokenTypes.IDENTIFIER)

        elif c.isdigit():
            numberBuilder = [char if char.isdigit() else "X" for char in self.origin[self.position :]]
            numberBuilder = "".join(numberBuilder).split("X")[0]

            self.position += len(numberBuilder) - 1
            self.actual = Token(numberBuilder, TokenTypes.NUMBER)

        else:
            self.logger.log(LogTypes.ERROR, f"Unknown character '{c}'")

    def isPositionValid(self, position: int):
        return position < len(self.origin)
