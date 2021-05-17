from abc import ABC, abstractmethod
from typing import List

from logger import logger
from symbolTable import SymbolTable
from tokens import Token, TokenTypes


class Node(ABC):
    value: Token
    children: List

    def __init__(self, value: Token, left: Token = None, right: Token = None) -> None:
        self.value = value
        self.children = [left, right]

    @abstractmethod
    def evaluate(self) -> int:
        return 0

    def setLeftChild(self, newChild: Token) -> None:
        self.children[0] = newChild

    def setRightChild(self, newChild: Token) -> None:
        self.children[1] = newChild

    def traverse(self, n, level=0):
        if n == None or len(n.children) == 0:
            return ""

        tabs: str = "\t" * int(level) if int(level) > 0 else ""
        if hasattr(n, "value"):
            outStr: str = f"{tabs}NT({type(n)}): NV({n.value})\n"
        else:
            outStr: str = f"{tabs}NT({type(n)})\n"

        if hasattr(n, "condition") and (type(n) == If or type(n) == While):
            outStr += self.traverse(n.condition, int(level + 1))

        for child in n.children:
            outStr += self.traverse(child, int(level + 1))

        return outStr

    def __str__(self) -> str:
        return self.traverse(self, 0)


class BinOp(Node):
    def __init__(self, value: Token, left: Token = None, right: Token = None) -> None:
        super().__init__(value=value, left=left, right=right)

    def evaluate(self, symbolTable: SymbolTable) -> int:
        if self.value.tokenType == TokenTypes.PLUS:
            return self.children[0].evaluate(symbolTable=symbolTable) + self.children[1].evaluate(symbolTable=symbolTable)
        elif self.value.tokenType == TokenTypes.MINUS:
            return self.children[0].evaluate(symbolTable=symbolTable) - self.children[1].evaluate(symbolTable=symbolTable)
        elif self.value.tokenType == TokenTypes.MULTIPLY:
            return self.children[0].evaluate(symbolTable=symbolTable) * self.children[1].evaluate(symbolTable=symbolTable)
        elif self.value.tokenType == TokenTypes.DIVIDE:
            return self.children[0].evaluate(symbolTable=symbolTable) / self.children[1].evaluate(symbolTable=symbolTable)


class UnOp(Node):
    def __init__(self, value: Token, left: Token) -> None:
        super().__init__(value=value, left=left)

    def evaluate(self, symbolTable: SymbolTable) -> int:
        if self.value.tokenType == TokenTypes.PLUS:
            return +self.children[0].evaluate(symbolTable=symbolTable)
        elif self.value.tokenType == TokenTypes.MINUS:
            return -self.children[0].evaluate(symbolTable=symbolTable)
        elif self.value.tokenType == TokenTypes.NOT:
            return not self.children[0].evaluate(symbolTable=symbolTable)


class IntVal(Node):
    def __init__(self, value: Token) -> None:
        super().__init__(value=value)

    def evaluate(self, symbolTable: SymbolTable) -> int:
        return int(self.value.value)


class NoOp(Node):
    def __init__(self, value: Token) -> None:
        super().__init__(value=value)

    def evaluate(self, symbolTable: SymbolTable) -> int:
        return 0


class Print(Node):
    def __init__(self, value: Token, left: Node) -> None:
        super().__init__(value=value, left=left)

    def evaluate(self, symbolTable: SymbolTable) -> None:
        print(int(self.children[0].evaluate(symbolTable=symbolTable)))


class Identifier(Node):
    def __init__(self, value: Token, left: Node) -> None:
        super().__init__(value=value, left=left)

    def evaluate(self, symbolTable: SymbolTable) -> None:
        varValue = self.children[0].evaluate(symbolTable=symbolTable)
        logger.debug(f"[Identifier] Setting variable {self.value} = {varValue}")
        symbolTable.setVar(var=self.value, value=varValue)


class Variable(Node):
    def __init__(self, value: Token) -> None:
        super().__init__(value=value)

    def evaluate(self, symbolTable: SymbolTable) -> int:
        return int(symbolTable.getVar(self.value.value))


class Readln(Node):
    def __init__(self, value: Token) -> None:
        super().__init__(value=value)

    def evaluate(self, symbolTable: SymbolTable) -> int:
        inputStr: str = str(input())
        if inputStr.isnumeric():
            return int(inputStr)
        else:
            logger.critical(f"[Readln] Input must be an integer: {inputStr}")


class Comparison(Node):
    def __init__(self, value: Node, left: Node, right: Node) -> None:
        super().__init__(value=value, left=left, right=right)

    def evaluate(self, symbolTable: SymbolTable) -> bool:
        leftSide: int = int(self.children[0].evaluate(symbolTable=symbolTable))
        rightSide: int = int(self.children[1].evaluate(symbolTable=symbolTable))
        logger.debug(f"[Comparison] Comparing {leftSide} ({self.value}) {rightSide}")

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
            logger.critical(f"[Comparison] Invalid comparison type: {self.value}")

        logger.debug(f"[Comparison] Result: {result}")
        return result


class Block(Node):
    children: List[Node]

    def __init__(self) -> None:
        self.children = []

    def evaluate(self, symbolTable: SymbolTable) -> None:
        for node in self.children:
            logger.debug(f"[Block] Running evaluate for {type(node)}")
            node.evaluate(symbolTable=symbolTable)

    def addNode(self, node: Node) -> None:
        self.children.append(node)


class If(Node):
    def __init__(self, value: Node, ifTrue: Node = None, ifFalse: Node = None, condition: Node = None) -> None:
        super().__init__(value=value, left=ifTrue, right=ifFalse)
        self.condition = condition

    def evaluate(self, symbolTable: SymbolTable) -> bool:
        conditionResult: bool = self.condition.evaluate(symbolTable=symbolTable)

        logger.debug(f"[If] Condition result: {conditionResult}")

        if conditionResult:
            return self.children[0].evaluate(symbolTable=symbolTable)
        elif self.children[1] != None:
            return self.children[1].evaluate(symbolTable=symbolTable)


class While(Node):
    def __init__(self, value: Node, command: Node = None, condition: Node = None) -> None:
        super().__init__(value=value, left=command)
        self.condition = condition

    def evaluate(self, symbolTable: SymbolTable) -> None:
        while self.condition.evaluate(symbolTable=symbolTable):
            self.children[0].evaluate(symbolTable=symbolTable)
