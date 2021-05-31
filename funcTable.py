from typing import Dict

from logger import logger


class FuncTable:
    table: Dict[str, str]

    def __init__(self) -> None:
        self.table = {}

    def getFunc(self, func: str) -> str:
        """
        Gets the Node for the given function name.
        """
        logger.debug(f"[FuncTable] Looking up function '{func}'")

        if func in self.table:
            return self.table[func]
        else:
            logger.critical(f"Unknown function '{func}'.")

    def setFunc(self, func: str, node: str) -> None:
        """
        Sets the value for the given variable name.
        """
        logger.debug(f"[FuncTable] Setting function '{func}'")

        if not self.declared(func):
            self.table[func] = node
        else:
            logger.critical(f"[FuncTable] Function '{func}' already declared")

    def declared(self, func: str) -> bool:
        """
        Returns 'true' if the variable has already been declared and 'false' if
        it hasn't.
        """
        if func in self.table:
            return True
        else:
            return False
