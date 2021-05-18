from logger import logger
from tokens import Token, TokenTypes
from varTypes import VarTypes


class Tokenizer:
    origin: str
    position: int
    actual: Token

    def __init__(self, code: str) -> None:
        self.origin = code
        self.position = -1
        self.actual = None

    def selectNext(self) -> None:
        """
        Sets 'self.actual' to the next valid token.
        """
        self.position += 1

        if not self.isPositionValid(self.position):
            self.actual = Token(None, TokenTypes.EOF)
            return

        c: str = self.origin[self.position]

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
                logger.critical(f"[Tokenizer] [SelectNext] Comparison with only one '|' is not allowed")

        elif c == "&":
            if self.isPositionValid(self.position + 1) and self.origin[self.position + 1] == "&":
                self.position += 1
                self.actual = Token("&&", TokenTypes.CMP_AND)
            else:
                logger.critical(f"[Tokenizer] [SelectNext] Comparison with only one '&' is not allowed")

        elif c == ";":
            self.actual = Token(c, TokenTypes.SEPARATOR)

        elif c == "{":
            self.actual = Token(c, TokenTypes.LEFT_BRACKET)

        elif c == "}":
            self.actual = Token(c, TokenTypes.RIGHT_BRACKET)

        elif c == '"':
            wordBuilder = [char if (char != '"') else '"' for char in self.origin[self.position + 1 :]]
            wordBuilder = "".join(wordBuilder).split('"')[0]
            self.position += len(wordBuilder)
            self.position += 1

            self.actual = Token(wordBuilder, TokenTypes.STRING_VALUE)

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
            elif wordBuilder == "int":
                self.actual = Token(wordBuilder, TokenTypes.TYPE, VarTypes.INT)
            elif wordBuilder == "bool":
                self.actual = Token(wordBuilder, TokenTypes.TYPE, VarTypes.BOOL)
            elif wordBuilder == "string":
                self.actual = Token(wordBuilder, TokenTypes.TYPE, VarTypes.STRING)
            elif wordBuilder in ["true", "false"]:
                self.actual = Token(wordBuilder, TokenTypes.BOOL_VALUE)
            else:
                self.actual = Token(wordBuilder, TokenTypes.IDENTIFIER)

        elif c.isdigit():
            numberBuilder = [char if char.isdigit() else "X" for char in self.origin[self.position :]]
            numberBuilder = "".join(numberBuilder).split("X")[0]

            self.position += len(numberBuilder) - 1
            self.actual = Token(numberBuilder, TokenTypes.NUMBER)

        else:
            logger.critical(f"[Tokenizer] [SelectNext] Unknown character found: '{c}'")

        logger.trace(f"[Tokenizer] [SelectNext] Actual: {self.actual}")

    def isPositionValid(self, position: int) -> bool:
        """
        Returns 'true' if the given position is less than the length
        of origin.
        """
        return position < len(self.origin)
