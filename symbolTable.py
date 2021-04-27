from typing import Dict
from node import Node
from logger import Logger, LogTypes


class SymbolTable:
    table: Dict[str, Node]
    logger: Logger

    def __init__(self, logger: Logger) -> None:
        self.table = {}
        self.logger = logger

    def getVar(self, var: str) -> Node:
        """
        Gets the value for the given variable name.
        """

        if var in self.table:
            return self.table[var]
        else:
            raise self.logger.log(LogTypes.ERROR, f"Unknown variable '{var}'.")

    def setVar(self, var: str, value: Node) -> None:
        """
        Sets the value for the given variable name.
        """

        self.table[var] = value
