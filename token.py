from enum import Enum


class TokenTypes(Enum):
    NUMBER = 1
    PLUS = 2
    MINUS = 3
    EOF = 4


class Token:
    tokenType: TokenTypes
    value: str

    def __init__(self, value: str, tokenType: TokenTypes):
        self.tokenType = tokenType
        self.value = value
