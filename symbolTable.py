from typing import Dict, Union

from logger import logger
from varTypes import Var, VarTypes


class SymbolTable:
    table: Dict[str, Dict[str, Union[int, bool, str]]]
    offsetEBP: int = 0
    intSize: int = 4
    boolSize: int = 4

    def __init__(self) -> None:
        self.table = {}

    def getVar(self, var: str) -> Union[VarTypes, Union[int, bool, str]]:
        """
        Gets the value for the given variable name.
        """
        logger.debug(f"[SymbolTable] [GetVar] Looking up variable '{var}'")

        if var in self.table:
            return Var(self.table[var]["type"], self.table[var]["value"]), self.table[var]["offset"]
        else:
            logger.critical(f"[SymbolTable] [GetVar] Unknown variable '{var}'.")

    def setVar(self, var: str, varType: VarTypes, value: Union[int, bool, str]) -> None:
        """
        Sets the value for the given variable name.
        """
        logger.debug(f"[SymbolTable] [SetVar] Setting/updating variable '{var}', as {varType}, with value '{value}'")

        if not self.declared(var):
            if varType == VarTypes.INT:
                self.offsetEBP += self.intSize
            elif varType == VarTypes.BOOL:
                self.offsetEBP += self.boolSize

            self.table[var] = {"type": varType, "value": value, "offset": self.offsetEBP}
        else:
            self.table[var] = {"type": varType, "value": value, "offset": self.getVarOffset(var)}

    def declared(self, var: str) -> bool:
        """
        Returns 'true' if the variable has already been declared and 'false' if
        it hasn't.
        """
        if var in self.table:
            return True
        else:
            return False

    def getVarOffset(self, var: str) -> int:
        if var in self.table:
            return self.table[var]["offset"]
        else:
            logger.critical(f"[SymbolTable] [GetVarOffset] Unknown variable '{var}'.")
