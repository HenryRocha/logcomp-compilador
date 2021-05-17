from typing import Dict, Union

from logger import logger


class SymbolTable:
    table: Dict[str, Union[int, bool]]

    def __init__(self) -> None:
        self.table = {}

    def getVar(self, var: str) -> int:
        """
        Gets the value for the given variable name.
        """
        logger.debug(f"[SymbolTable] Looking up variable '{var}'")

        if var in self.table:
            return self.table[var]
        else:
            logger.critical(f"Unknown variable '{var}'.")

    def setVar(self, var: str, value) -> None:
        """
        Sets the value for the given variable name.
        """
        logger.debug(f"[SymbolTable] Setting/updating variable '{var}'")

        self.table[var] = value
