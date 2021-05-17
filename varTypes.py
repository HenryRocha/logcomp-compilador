from enum import Enum


class VarTypes(Enum):
    INT = 1
    BOOL = 2
    STRING = 3


class Var:
    varType: VarTypes
    value: str

    def __init__(self, varType: VarTypes, value: str) -> None:
        self.varType = varType
        self.value = value

    def __str__(self) -> str:
        return f"VT({self.varType}): VV({self.value})"
