from abc import ABC, abstractmethod
from typing import List

from logger import logger
from symbolTable import SymbolTable
from tokens import Token, TokenTypes
from varTypes import Var, VarTypes


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
        var1: Var = self.children[0].evaluate(symbolTable=symbolTable)
        var2: Var = self.children[1].evaluate(symbolTable=symbolTable)

        if (var1.varType in [VarTypes.INT, VarTypes.BOOL] and var2.varType == VarTypes.STRING) or (
            var1.varType == VarTypes.STRING and var2.varType in [VarTypes.INT, VarTypes.BOOL]
        ):
            logger.critical(f"[BinOp] Variable types are different. {var1.varType} != {var2.varType}")

        logger.debug(f"[BinOp] Adding {var1} + {var1}")

        if self.value.tokenType == TokenTypes.PLUS:
            return Var(VarTypes.INT, var1.value + var2.value)
        elif self.value.tokenType == TokenTypes.MINUS:
            return Var(VarTypes.INT, var1.value - var2.value)
        elif self.value.tokenType == TokenTypes.MULTIPLY:
            return Var(VarTypes.INT, var1.value * var2.value)
        elif self.value.tokenType == TokenTypes.DIVIDE:
            return Var(VarTypes.INT, var1.value // var2.value)


class UnOp(Node):
    def __init__(self, value: Token, left: Token) -> None:
        super().__init__(value=value, left=left)

    def evaluate(self, symbolTable: SymbolTable) -> int:
        var: Var = self.children[0].evaluate(symbolTable=symbolTable)

        if self.value.tokenType == TokenTypes.PLUS:
            return Var(VarTypes.INT, +var.value)
        elif self.value.tokenType == TokenTypes.MINUS:
            return Var(VarTypes.INT, -var.value)
        elif self.value.tokenType == TokenTypes.NOT:
            return Var(VarTypes.BOOL, not bool(var.value))


class IntVal(Node):
    def __init__(self, value: Token) -> None:
        super().__init__(value=value)

    def evaluate(self, symbolTable: SymbolTable) -> int:
        return Var(VarTypes.INT, int(self.value.value))


class NoOp(Node):
    def __init__(self, value: Token) -> None:
        super().__init__(value=value)

    def evaluate(self, symbolTable: SymbolTable) -> int:
        return Var(VarTypes.INT, 0)


class Print(Node):
    def __init__(self, value: Token, left: Node) -> None:
        super().__init__(value=value, left=left)

    def evaluate(self, symbolTable: SymbolTable) -> None:
        print(self.children[0].evaluate(symbolTable=symbolTable).value)


class Identifier(Node):
    def __init__(self, value: Token, left: Node, varType: VarTypes = None) -> None:
        super().__init__(value=value, left=left)
        self.varType = varType

    def evaluate(self, symbolTable: SymbolTable) -> None:
        if not symbolTable.declared(self.value):
            if self.varType == None:
                logger.critical(f"[Identifier] Missing type on declaration for variable '{self.value}'")

            var: Var = self.children[0].evaluate(symbolTable=symbolTable)
            logger.debug(f"[Identifier] Setting variable ({self.varType}) {self.value} = {var.value}")
            symbolTable.setVar(var=self.value, varType=self.varType, value=var.value)
        else:
            if self.varType != None:
                logger.critical(f"[Identifier] Variable '{self.value}' already declared. Type: {self.varType}")

            var: Var = self.children[0].evaluate(symbolTable=symbolTable)
            existingVar: Var = symbolTable.getVar(var=self.value)
            if (existingVar.varType in [VarTypes.INT, VarTypes.BOOL] and var.varType == VarTypes.STRING) or (
                existingVar.varType == VarTypes.STRING and var.varType in [VarTypes.INT, VarTypes.BOOL]
            ):
                logger.critical(
                    f"[Identifier] Variable reassign with mismatching types. '{self.value}' has type {existingVar.varType} but was reassigned to {var.varType}"
                )

            logger.debug(f"[Identifier] Setting variable ({var.varType}) {self.value} = {var.value}")

            if existingVar.varType == VarTypes.INT:
                symbolTable.setVar(var=self.value, varType=var.varType, value=int(var.value))
            elif existingVar.varType == VarTypes.BOOL:
                symbolTable.setVar(var=self.value, varType=var.varType, value=bool(var.value))
            elif existingVar.varType == VarTypes.STRING:
                symbolTable.setVar(var=self.value, varType=var.varType, value=str(var.value))


class Variable(Node):
    def __init__(self, value: Token) -> None:
        super().__init__(value=value)

    def evaluate(self, symbolTable: SymbolTable) -> int:
        return symbolTable.getVar(self.value.value)


class Readln(Node):
    def __init__(self, value: Token) -> None:
        super().__init__(value=value)

    def evaluate(self, symbolTable: SymbolTable) -> int:
        inputStr: str = str(input())
        if inputStr.isnumeric():
            return Var(VarTypes.INT, int(inputStr))
        else:
            logger.critical(f"[Readln] Input must be an integer: {inputStr}")


class Comparison(Node):
    def __init__(self, value: Node, left: Node, right: Node) -> None:
        super().__init__(value=value, left=left, right=right)

    def evaluate(self, symbolTable: SymbolTable) -> bool:
        leftSide: Var = self.children[0].evaluate(symbolTable=symbolTable)
        rightSide: Var = self.children[1].evaluate(symbolTable=symbolTable)
        logger.debug(f"[Comparison] Comparing {leftSide} ({self.value}) {rightSide}")

        if (leftSide.varType in [VarTypes.INT, VarTypes.BOOL] and rightSide.varType == VarTypes.STRING) or (
            leftSide.varType == VarTypes.STRING and rightSide.varType in [VarTypes.INT, VarTypes.BOOL]
        ):
            logger.critical(f"[BinOp] Variable types are different. {leftSide.varType} != {rightSide.varType}")

        result: bool = False
        if self.value.tokenType == TokenTypes.CMP_EQUAL:
            result = bool(leftSide.value == rightSide.value)
        elif self.value.tokenType == TokenTypes.CMP_GREATER:
            result = bool(leftSide.value > rightSide.value)
        elif self.value.tokenType == TokenTypes.CMP_LESS:
            result = bool(leftSide.value < rightSide.value)
        elif self.value.tokenType == TokenTypes.CMP_AND:
            result = bool(leftSide.value) and bool(rightSide.value)
        elif self.value.tokenType == TokenTypes.CMP_OR:
            result = bool(leftSide.value) or bool(rightSide.value)
        else:
            logger.critical(f"[Comparison] Invalid comparison type: {self.value}")

        logger.debug(f"[Comparison] Result: {result}")
        return Var(VarTypes.BOOL, result)


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

        if conditionResult.value:
            return self.children[0].evaluate(symbolTable=symbolTable)
        elif self.children[1] != None:
            return self.children[1].evaluate(symbolTable=symbolTable)


class While(Node):
    def __init__(self, value: Node, command: Node = None, condition: Node = None) -> None:
        super().__init__(value=value, left=command)
        self.condition = condition

    def evaluate(self, symbolTable: SymbolTable) -> None:
        while self.condition.evaluate(symbolTable=symbolTable).value:
            self.children[0].evaluate(symbolTable=symbolTable)


class BoolVal(Node):
    def __init__(self, value: Token) -> None:
        if value.value in ["true", "false"]:
            super().__init__(value=value)
        else:
            logger.critical(f"[BoolVal] Value is not 'true'/'false': {value}")

    def evaluate(self, symbolTable: SymbolTable) -> bool:
        if self.value.value == "true":
            return Var(VarTypes.BOOL, True)
        else:
            return Var(VarTypes.BOOL, False)


class StringVal(Node):
    def __init__(self, value: Token) -> None:
        super().__init__(value=value)

    def evaluate(self, symbolTable: SymbolTable) -> str:
        return Var(VarTypes.STRING, self.value.value)
