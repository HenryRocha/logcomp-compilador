from enum import Enum


class TokenTypes(Enum):
    NUMBER = 1
    PLUS = 2
    MINUS = 3
    MULTIPLY = 4
    DIVIDE = 5
    LEFT_PARENTHESIS = 6
    RIGHT_PARENTHESIS = 7
    EOF = 8


class Token:
    tokenType: TokenTypes
    value: str

    def __init__(self, value: str, tokenType: TokenTypes):
        self.tokenType = tokenType
        self.value = value

    def __str__(self):
        return f"{self.tokenType} => {self.value}"
