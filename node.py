from abc import ABC, abstractmethod
from tokens import Token, TokenTypes
from symbolTable import SymbolTable
from logger import Logger, LogTypes


class Node(ABC):
    value: Token
    children: []

    def __init__(self, value: Token, left: Token = None, right: Token = None):
        self.value = value
        self.children = [left, right]

    @abstractmethod
    def evaluate(self) -> int:
        return 0

    def setLeftChild(self, newChild: Token) -> None:
        self.children[0] = newChild

    def setRightChild(self, newChild: Token) -> None:
        self.children[1] = newChild

    def __str__(self):
        return f"{self.value}"


class BinOp(Node):
    def __init__(self, value: Token, left: Token = None, right: Token = None):
        super().__init__(value=value, left=left, right=right)

    def evaluate(self, symbolTable: SymbolTable, logger: Logger) -> int:
        if self.value.tokenType == TokenTypes.PLUS:
            return self.children[0].evaluate(symbolTable=symbolTable, logger=logger) + self.children[1].evaluate(
                symbolTable=symbolTable, logger=logger
            )
        elif self.value.tokenType == TokenTypes.MINUS:
            return self.children[0].evaluate(symbolTable=symbolTable, logger=logger) - self.children[1].evaluate(
                symbolTable=symbolTable, logger=logger
            )
        elif self.value.tokenType == TokenTypes.MULTIPLY:
            return self.children[0].evaluate(symbolTable=symbolTable, logger=logger) * self.children[1].evaluate(
                symbolTable=symbolTable, logger=logger
            )
        elif self.value.tokenType == TokenTypes.DIVIDE:
            return self.children[0].evaluate(symbolTable=symbolTable, logger=logger) / self.children[1].evaluate(
                symbolTable=symbolTable, logger=logger
            )


class UnOp(Node):
    def __init__(self, value: Token, left: Token):
        super().__init__(value=value, left=left)

    def evaluate(self, symbolTable: SymbolTable, logger: Logger) -> int:
        if self.value.tokenType == TokenTypes.PLUS:
            return +self.children[0].evaluate(symbolTable=symbolTable, logger=logger)
        elif self.value.tokenType == TokenTypes.MINUS:
            return -self.children[0].evaluate(symbolTable=symbolTable, logger=logger)
        elif self.value.tokenType == TokenTypes.NOT:
            return not self.children[0].evaluate(symbolTable=symbolTable, logger=logger)


class IntVal(Node):
    def __init__(self, value: Token):
        super().__init__(value=value)

    def evaluate(self, symbolTable: SymbolTable, logger: Logger) -> int:
        return int(self.value.value)


class NoOp(Node):
    def __init__(self, value: Token):
        super().__init__(value=value)

    def evaluate(self, symbolTable: SymbolTable, logger: Logger) -> int:
        return 0


class Print(Node):
    def __init__(self, value: Token, left: Node):
        super().__init__(value=value, left=left)

    def evaluate(self, symbolTable: SymbolTable, logger: Logger) -> None:
        print(int(self.children[0].evaluate(symbolTable=symbolTable, logger=logger)))


class Identifier(Node):
    def __init__(self, value: Token, left: Node):
        super().__init__(value=value, left=left)

    def evaluate(self, symbolTable: SymbolTable, logger: Logger) -> None:
        varValue = self.children[0].evaluate(symbolTable=symbolTable, logger=logger)
        logger.log(LogTypes.NORMAL, f"Setting variable {self.value} = {varValue}")
        symbolTable.setVar(var=self.value, value=varValue)


class Variable(Node):
    def __init__(self, value: Token):
        super().__init__(value=value)

    def evaluate(self, symbolTable: SymbolTable, logger: Logger) -> int:
        return int(symbolTable.getVar(self.value.value))


class Readln(Node):
    def __init__(self, value: Token):
        super().__init__(value=value)

    def evaluate(self, symbolTable: SymbolTable, logger: Logger) -> int:
        inputStr: str = str(input())
        if inputStr.isnumeric():
            return int(inputStr)
        else:
            raise ValueError("Readln input must be an integer")


class Comparison(Node):
    def __init__(self, value: Node, left: Node, right: Node):
        super().__init__(value=value, left=left, right=right)

    def evaluate(self, symbolTable: SymbolTable, logger: Logger) -> bool:
        leftSide: int = int(self.children[0].evaluate(symbolTable=symbolTable, logger=logger))
        rightSide: int = int(self.children[1].evaluate(symbolTable=symbolTable, logger=logger))
        logger.log(LogTypes.NORMAL, f"[LOG] Comparing {leftSide} ({self.value}) {rightSide}")

        result: bool = False
        if self.value.tokenType == TokenTypes.CMP_EQUAL:
            result = leftSide == rightSide
        elif self.value.tokenType == TokenTypes.CMP_GREATER:
            result = leftSide > rightSide
        elif self.value.tokenType == TokenTypes.CMP_LESS:
            result = leftSide < rightSide
        elif self.value.tokenType == TokenTypes.CMP_AND:
            result = bool(leftSide) and bool(rightSide)
        elif self.value.tokenType == TokenTypes.CMP_OR:
            result = bool(leftSide) or bool(rightSide)
        else:
            raise ValueError(f"Invalid comparison type: {self.value}")

        logger.log(LogTypes.NORMAL, f"Result: {result}")
        return result


class Block(Node):
    children: [Node]

    def __init__(self):
        self.children = []

    def evaluate(self, symbolTable: SymbolTable, logger: Logger) -> None:
        for node in self.children:
            logger.log(LogTypes.NORMAL, f"Running evaluate for {type(node)}")
            node.evaluate(symbolTable=symbolTable, logger=logger)

    def addNode(self, node: Node):
        self.children.append(node)


class If(Node):
    def __init__(self, value: Node, ifTrue: Node = None, ifFalse: Node = None, condition: Node = None):
        super().__init__(value=value, left=ifTrue, right=ifFalse)
        self.condition = condition

    def evaluate(self, symbolTable: SymbolTable, logger: Logger) -> bool:
        if self.condition.evaluate(symbolTable=symbolTable, logger=logger):
            return self.children[0].evaluate(symbolTable=symbolTable, logger=logger)
        else:
            return self.children[1].evaluate(symbolTable=symbolTable, logger=logger)

    def __str__(self) -> str:
        outputStr: str = f"NODE: {self.value}\n"
        outputStr += f"\tIFTRUE: {self.children[0].value}"
        outputStr += f"\tIFFALSE: {self.children[1].value}"
        outputStr += f"\tCONDITION: {self.condition.value}"
        return outputStr


class While(Node):
    def __init__(self, value: Node, command: Node = None, condition: Node = None):
        super().__init__(value=value, left=command)
        self.condition = condition

    def evaluate(self, symbolTable: SymbolTable, logger: Logger) -> None:
        while self.condition.evaluate(symbolTable=symbolTable, logger=logger):
            self.children[0].evaluate(symbolTable=symbolTable, logger=logger)
