from enum import Enum

from varTypes import VarTypes


class TokenTypes(Enum):
    NUMBER = 1
    PLUS = 2
    MINUS = 3
    MULTIPLY = 4
    DIVIDE = 5
    LEFT_PARENTHESIS = 6
    RIGHT_PARENTHESIS = 7
    EOF = 8
    IDENTIFIER = 9
    ASSIGN = 10
    SEPARATOR = 11
    PRINT = 12
    READLN = 13
    CMP_EQUAL = 14
    CMP_GREATER = 15
    CMP_LESS = 16
    CMP_AND = 17
    CMP_OR = 18
    NOT = 19
    WHILE = 20
    IF = 21
    ELSE = 22
    LEFT_BRACKET = 23
    RIGHT_BRACKET = 24
    TYPE = 25
    BOOL_VALUE = 26
    STRING_VALUE = 27
    PARAM_SEPARATOR = 28
    RETURN = 29


class Token:
    tokenType: TokenTypes
    value: str
    varType: VarTypes

    def __init__(self, value: str, tokenType: TokenTypes, varType: VarTypes = None) -> None:
        self.tokenType = tokenType
        self.value = value
        self.varType = varType

    def __str__(self) -> str:
        return f"TT({self.tokenType}): TV({self.value})"
