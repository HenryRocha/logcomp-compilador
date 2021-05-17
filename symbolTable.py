from typing import Dict, Union

from logger import logger
from varTypes import Var, VarTypes


class SymbolTable:
    table: Dict[str, Dict[str, Union[int, bool, str]]]

    def __init__(self) -> None:
        self.table = {}

    def getVar(self, var: str) -> Union[VarTypes, Union[int, bool, str]]:
        """
        Gets the value for the given variable name.
        """
        logger.debug(f"[SymbolTable] Looking up variable '{var}'")

        if var in self.table:
            return Var(self.table[var]["type"], self.table[var]["value"])
        else:
            logger.critical(f"Unknown variable '{var}'.")

    def setVar(self, var: str, varType: VarTypes, value: Union[int, bool, str]) -> None:
        """
        Sets the value for the given variable name.
        """
        logger.debug(f"[SymbolTable] Setting/updating variable '{var}', as {varType}, with value '{value}'")

        self.table[var] = {"type": varType, "value": value}

    def declared(self, var: str) -> bool:
        """
        Returns 'true' if the variable has already been declared and 'false' if
        it hasn't.
        """
        if var in self.table:
            return True
        else:
            return False
