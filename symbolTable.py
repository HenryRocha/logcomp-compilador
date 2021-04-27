from typing import Dict
from logger import Logger, LogTypes


class SymbolTable:
    logger: Logger

    def __init__(self, logger: Logger) -> None:
        self.table = {}
        self.logger = logger

    def getVar(self, var: str):
        """
        Gets the value for the given variable name.
        """
        self.logger.log(LogTypes.NORMAL, f"Looking up variable '{var}'")

        if var in self.table:
            return self.table[var]
        else:
            raise self.logger.log(LogTypes.ERROR, f"Unknown variable '{var}'.")

    def setVar(self, var: str, value) -> None:
        """
        Sets the value for the given variable name.
        """
        self.logger.log(LogTypes.NORMAL, f"Setting/updating variable '{var}'")

        self.table[var] = value
