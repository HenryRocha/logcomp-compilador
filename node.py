import uuid
from abc import ABC, abstractmethod
from typing import List

from assembly import assembly
from logger import logger
from symbolTable import SymbolTable
from tokens import Token, TokenTypes
from varTypes import Var, VarTypes


class Node(ABC):
    value: Token
    children: List
    nid: int

    def __init__(self, value: Token, left: Token = None, right: Token = None) -> None:
        self.value = value
        self.children = [left, right]
        self.nid = uuid.uuid4().hex

    @abstractmethod
    def evaluate(self) -> int:
        return 0

    def toHex(self, val: int, nbits: int = 32) -> str:
        return hex((val + (1 << nbits)) % (1 << nbits))

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
        assembly.writeComment("BinOp START\n")

        var1: Var = self.children[0].evaluate(symbolTable=symbolTable)
        assembly.writeInstruction(f"PUSH EBX; BinOp store var1")

        var2: Var = self.children[1].evaluate(symbolTable=symbolTable)
        assembly.writeInstruction(f"POP EAX; BinOp restore var1 to EAX")

        if (var1.varType in [VarTypes.INT, VarTypes.BOOL] and var2.varType == VarTypes.STRING) or (
            var1.varType == VarTypes.STRING and var2.varType in [VarTypes.INT, VarTypes.BOOL]
        ):
            logger.critical(f"[BinOp] Variable types are different. {var1.varType} != {var2.varType}")

        logger.debug(f"[BinOp] {var1} {self.value} {var1}")

        if self.value.tokenType == TokenTypes.PLUS:
            assembly.writeInstruction(f"ADD EAX, EBX; BinOp ADD")
            assembly.writeInstruction(f"MOV EBX, EAX;")
            res: Var = Var(VarTypes.INT, var1.value + var2.value)
        elif self.value.tokenType == TokenTypes.MINUS:
            assembly.writeInstruction(f"SUB EAX, EBX; BinOp SUB")
            assembly.writeInstruction(f"MOV EBX, EAX;")
            res: Var = Var(VarTypes.INT, var1.value - var2.value)
        elif self.value.tokenType == TokenTypes.MULTIPLY:
            assembly.writeInstruction(f"IMUL EBX; BinOp MULT")
            assembly.writeInstruction(f"MOV EBX, EAX;")
            res: Var = Var(VarTypes.INT, var1.value * var2.value)
        elif self.value.tokenType == TokenTypes.DIVIDE:
            assembly.writeInstruction(f"DIV EBX; BinOp DIV")
            assembly.writeInstruction(f"MOV EBX, EAX;")
            res: Var = Var(VarTypes.INT, var1.value // var2.value)

        assembly.writeComment(f"BinOp END, RES = {res.value}\n")
        return res


class UnOp(Node):
    def __init__(self, value: Token, left: Token) -> None:
        super().__init__(value=value, left=left)

    def evaluate(self, symbolTable: SymbolTable) -> int:
        assembly.writeComment("UnOp START")

        var: Var = self.children[0].evaluate(symbolTable=symbolTable)

        if self.value.tokenType == TokenTypes.PLUS:
            assembly.writeComment("UnOp END\n")
            return Var(VarTypes.INT, +var.value)
        elif self.value.tokenType == TokenTypes.MINUS:
            assembly.writeInstruction(f"MOV EAX, {self.toHex(-1)} ; UnOp MINUS")
            assembly.writeInstruction(f"IMUL EBX; UnOp MINUS")
            assembly.writeInstruction(f"MOV EBX, EAX; UnOp MINUS")
            assembly.writeComment("UnOp END\n")
            return Var(VarTypes.INT, -var.value)
        elif self.value.tokenType == TokenTypes.NOT:
            res: bool = not bool(var.value)
            assembly.writeInstruction(f"CMP EBX, 0; UnOp NOT")
            assembly.writeInstruction(f"CALL binop_je; UnOp NOT")
            assembly.writeComment("UnOp END\n")
            return Var(VarTypes.BOOL, res)


class IntVal(Node):
    def __init__(self, value: Token) -> None:
        super().__init__(value=value)

    def evaluate(self, symbolTable: SymbolTable) -> int:
        value: int = int(self.value.value)

        assembly.writeComment("IntVal START")
        assembly.writeInstruction(f"MOV EBX, {value}; IntVal = {value}")
        assembly.writeComment("IntVal END\n")

        return Var(VarTypes.INT, value)


class NoOp(Node):
    def __init__(self, value: Token) -> None:
        super().__init__(value=value)

    def evaluate(self, symbolTable: SymbolTable) -> int:
        assembly.writeInstruction("NOP ; NoOp")
        return Var(VarTypes.INT, 0)


class Print(Node):
    def __init__(self, value: Token, left: Node) -> None:
        super().__init__(value=value, left=left)

    def evaluate(self, symbolTable: SymbolTable) -> None:
        self.children[0].evaluate(symbolTable=symbolTable).value

        assembly.writeComment("Print START")
        assembly.writeInstruction(f"PUSH EBX; Print store child result")
        assembly.writeInstruction(f"CALL print;")
        assembly.writeInstruction(f"POP EBX; Print delete child result")

        # Print "\n"
        assembly.writeInstruction(f"MOV EAX, SYS_WRITE;")
        assembly.writeInstruction(f"MOV EBX, STDOUT;")
        assembly.writeInstruction(f"MOV ECX, NEWLINE;")
        assembly.writeInstruction(f"MOV EDX, 1;")
        assembly.writeInstruction(f"INT 0x80;")
        assembly.writeComment("Print END\n")


class Identifier(Node):
    def __init__(self, value: Token, left: Node, varType: VarTypes = None) -> None:
        super().__init__(value=value, left=left)
        self.varType = varType

    def evaluate(self, symbolTable: SymbolTable) -> None:
        assembly.writeComment("Identifier START")

        if not symbolTable.declared(self.value):
            if self.varType == None:
                logger.critical(f"[Identifier] Missing type on declaration for variable '{self.value}'")

            assembly.writeInstruction(f"PUSH DWORD 0; Identifier {self.value} first atribution\n")

            var: Var = self.children[0].evaluate(symbolTable=symbolTable)

            logger.debug(f"[Identifier] Setting variable ({self.varType}) {self.value} = {var.value}")
            symbolTable.setVar(var=self.value, varType=self.varType, value=var.value)

            assembly.writeInstruction(f"MOV [EBP - {symbolTable.getVarOffset(self.value)}], EBX; Identifier store variable {self.value}")
        else:
            if self.varType != None:
                logger.critical(f"[Identifier] Variable '{self.value}' already declared. Type: {self.varType}")

            var: Var = self.children[0].evaluate(symbolTable=symbolTable)
            existingVar, _ = symbolTable.getVar(var=self.value)
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

            assembly.writeInstruction(f"MOV [EBP - {symbolTable.getVarOffset(self.value)}], EBX; Identifier setting/updating variable {self.value}")

        assembly.writeComment("Identifier END\n")


class Variable(Node):
    def __init__(self, value: Token) -> None:
        super().__init__(value=value)

    def evaluate(self, symbolTable: SymbolTable) -> int:
        var, offset = symbolTable.getVar(self.value.value)

        assembly.writeComment("Variable START")
        assembly.writeInstruction(f"MOV EBX, [EBP - {offset}]; Variable lookup for {self.value.value}")
        assembly.writeComment("Variable END\n")

        return var


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
        assembly.writeComment("Comparison START")

        leftSide: Var = self.children[0].evaluate(symbolTable=symbolTable)
        assembly.writeInstruction(f"PUSH EBX; Comparison store leftSide")

        rightSide: Var = self.children[1].evaluate(symbolTable=symbolTable)
        assembly.writeInstruction(f"POP EAX; Comparison restore leftSide to EAX")

        logger.debug(f"[Comparison] Comparing {leftSide} ({self.value}) {rightSide}")

        if (leftSide.varType in [VarTypes.INT, VarTypes.BOOL] and rightSide.varType == VarTypes.STRING) or (
            leftSide.varType == VarTypes.STRING and rightSide.varType in [VarTypes.INT, VarTypes.BOOL]
        ):
            logger.critical(f"[BinOp] Variable types are different. {leftSide.varType} != {rightSide.varType}")

        result: bool = False
        if self.value.tokenType == TokenTypes.CMP_EQUAL:
            assembly.writeInstruction(f"CMP EAX, EBX; Comparison EQUAL")
            assembly.writeInstruction(f"CALL binop_je; Comparison GREATER")
            result = bool(leftSide.value == rightSide.value)
        elif self.value.tokenType == TokenTypes.CMP_GREATER:
            assembly.writeInstruction(f"CMP EAX, EBX; Comparison GREATER")
            assembly.writeInstruction(f"CALL binop_jg; Comparison GREATER")
            result = bool(leftSide.value > rightSide.value)
        elif self.value.tokenType == TokenTypes.CMP_LESS:
            assembly.writeInstruction(f"CMP EAX, EBX; Comparison LESS")
            assembly.writeInstruction(f"CALL binop_jl; Comparison LESS")
            result = bool(leftSide.value < rightSide.value)
        elif self.value.tokenType == TokenTypes.CMP_AND:
            result = bool(leftSide.value) and bool(rightSide.value)
            assembly.writeInstruction(f"AND EBX, EAX; Comparison AND")
        elif self.value.tokenType == TokenTypes.CMP_OR:
            assembly.writeInstruction(f"OR EBX, EAX; Comparison OR")
            result = bool(leftSide.value) or bool(rightSide.value)
        else:
            logger.critical(f"[Comparison] Invalid comparison type: {self.value}")

        assembly.writeComment("Comparison END\n")

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
        conditionResult: Var = self.condition.evaluate(symbolTable=symbolTable)
        logger.debug(f"[If] Condition result: {conditionResult}")

        if conditionResult.varType == VarTypes.STRING:
            logger.critical(f"[If] Condition cannot be a STRING: {conditionResult}")

        assembly.writeComment("If START")
        assembly.writeInstruction("CMP EBX, False; If comparison")
        assembly.writeInstruction(f"JE IF_ELSE_{self.nid}; If false jump")

        self.children[0].evaluate(symbolTable=symbolTable)
        assembly.writeInstruction(f"JMP IF_{self.nid}_EXIT; If true jump")

        assembly.writeInstruction(f"IF_ELSE_{self.nid}: ; If else")
        if self.children[1] != None:
            self.children[1].evaluate(symbolTable=symbolTable)

        assembly.writeInstruction(f"IF_{self.nid}_EXIT: ; If exit")
        assembly.writeComment("If END\n")


class While(Node):
    def __init__(self, value: Node, command: Node = None, condition: Node = None) -> None:
        super().__init__(value=value, left=command)
        self.condition = condition

    def evaluate(self, symbolTable: SymbolTable) -> None:
        assembly.writeComment("While START")
        assembly.writeInstruction(f"WHILE_{self.nid}: ; While start")

        condition: Var = self.condition.evaluate(symbolTable=symbolTable)

        assembly.writeInstruction(f"CMP EBX, False; While first compare")
        assembly.writeInstruction(f"JE WHILE_{self.nid}_EXIT; While first stop")

        if condition.value:
            self.children[0].evaluate(symbolTable=symbolTable)
            condition: Var = self.condition.evaluate(symbolTable=symbolTable)

        assembly.writeInstruction(f"JMP WHILE_{self.nid}; While loop")
        assembly.writeInstruction(f"WHILE_{self.nid}_EXIT: ; While final stop stop")
        assembly.writeComment("While END\n")


class BoolVal(Node):
    def __init__(self, value: Token) -> None:
        if value.value in ["true", "false"]:
            super().__init__(value=value)
        else:
            logger.critical(f"[BoolVal] Value is not 'true'/'false': {value}")

    def evaluate(self, symbolTable: SymbolTable) -> bool:
        assembly.writeComment("BoolVal START")
        if self.value.value == "true":
            assembly.writeInstruction("MOV EBX, 1; BoolVal TRUE")
            assembly.writeComment("BoolVal END\n")
            return Var(VarTypes.BOOL, True)
        else:
            assembly.writeInstruction("MOV EBX, 0; BoolVal FALSE")
            assembly.writeComment("BoolVal END\n")
            return Var(VarTypes.BOOL, False)


class StringVal(Node):
    def __init__(self, value: Token) -> None:
        super().__init__(value=value)

    def evaluate(self, symbolTable: SymbolTable) -> str:
        return Var(VarTypes.STRING, self.value.value)
