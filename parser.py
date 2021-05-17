from typing import List
from varTypes import VarTypes

from logger import logger
from node import BinOp, Block, Comparison, Identifier, If, IntVal, Node, NoOp, Print, Readln, UnOp, Variable, While
from preprocess import PreProcess
from symbolTable import SymbolTable
from tokenizer import Tokenizer
from tokens import Token, TokenTypes


class Parser:
    OPERATORS: List[TokenTypes] = [TokenTypes.PLUS, TokenTypes.MINUS, TokenTypes.MULTIPLY, TokenTypes.DIVIDE]
    MARKERS: List[TokenTypes] = [TokenTypes.LEFT_PARENTHESIS, TokenTypes.RIGHT_PARENTHESIS, TokenTypes.SEPARATOR]
    CMPS: List[TokenTypes] = [TokenTypes.CMP_EQUAL, TokenTypes.CMP_GREATER, TokenTypes.CMP_LESS, TokenTypes.CMP_AND, TokenTypes.CMP_OR]
    tokens: Tokenizer
    symbolTable: SymbolTable
    result: int

    def __init__(self) -> None:
        self.symbolTable = SymbolTable()

    def parseBlock(self) -> Node:
        logger.info(f"[ParseBlock] Start...")

        ret: Node = Block()

        if self.tokens.actual.tokenType != TokenTypes.LEFT_BRACKET:
            logger.critical(f"[ParseBlock] Block cannot start with {self.tokens.actual}")

        self.tokens.selectNext()
        while self.tokens.actual.tokenType != TokenTypes.RIGHT_BRACKET:
            ret.addNode(self.parseCommand())
            logger.debug(f"[ParseBlock] Actual: {self.tokens.actual}")
            self.tokens.selectNext()

        logger.info(f"[ParseBlock] End")
        return ret

    def parseCommand(self) -> Node:
        logger.info(f"[ParseCommand] Start...")

        ret: Node = NoOp(Token("", TokenTypes.EOF))

        if self.tokens.actual.tokenType == TokenTypes.TYPE:
            logger.debug(f"[ParseCommand] Consumed TYPE '{self.tokens.actual}'")

            varType: VarTypes = self.tokens.actual.varType

            self.tokens.selectNext()
            if self.tokens.actual.tokenType != TokenTypes.IDENTIFIER:
                logger.critical(f"[ParseCommand] TYPE is followed by '{self.tokens.actual}' instead of IDENTIFIER")

            variableName: str = self.tokens.actual.value

            self.tokens.selectNext()
            if self.tokens.actual.tokenType != TokenTypes.ASSIGN:
                logger.critical(f"[ParseCommand] IDENTIFIER is followed by '{self.tokens.actual}' instead of '='")

            logger.trace(f"[ParseCommand] Creating IDENTIFIER's AST...")
            ret = Identifier(value=variableName, varType=varType, left=self.parseOrExpr())
            logger.trace(f"[ParseCommand] Finished creating IDENTIFIER's AST...")

            if self.tokens.actual.tokenType != TokenTypes.SEPARATOR:
                logger.critical(f"[ParseCommand] IDENTIFIER's expression is followed by '{self.tokens.actual}' instead of ';'")

        elif self.tokens.actual.tokenType == TokenTypes.IDENTIFIER:
            logger.debug(f"[ParseCommand] Consumed IDENTIFIER '{self.tokens.actual}'")
            variableName: str = self.tokens.actual.value

            self.tokens.selectNext()
            if self.tokens.actual.tokenType != TokenTypes.ASSIGN:
                logger.critical(f"[ParseCommand] IDENTIFIER is followed by '{self.tokens.actual}' instead of '='")

            logger.trace(f"[ParseCommand] Creating IDENTIFIER's AST...")
            ret = Identifier(value=variableName, left=self.parseOrExpr())
            logger.trace(f"[ParseCommand] Finished creating IDENTIFIER's AST...")

            if self.tokens.actual.tokenType != TokenTypes.SEPARATOR:
                logger.critical(f"[ParseCommand] IDENTIFIER's expression is followed by '{self.tokens.actual}' instead of ';'")

        elif self.tokens.actual.tokenType == TokenTypes.PRINT:
            logger.debug(f"[ParseCommand] Consumed PRINTLN '{self.tokens.actual}'")

            self.tokens.selectNext()
            if self.tokens.actual.tokenType != TokenTypes.LEFT_PARENTHESIS:
                logger.critical(f"[ParseCommand] PRINTLN is followed by '{self.tokens.actual}' instead of '('")

            logger.trace(f"[ParseCommand] Creating PRINTLN's AST...")
            ret = Print(value=Token("println", TokenTypes.PRINT), left=self.parseOrExpr())
            logger.trace(f"[ParseCommand] Finished creating PRINTLN's AST...")

            if self.tokens.actual.tokenType != TokenTypes.RIGHT_PARENTHESIS:
                logger.critical(f"[ParseCommand] PRINTLN's expression is followed by '{self.tokens.actual}' instead of ')'")

            self.tokens.selectNext()
            if self.tokens.actual.tokenType != TokenTypes.SEPARATOR:
                logger.critical(f"[ParseCommand] PRINTLN's ')' is followed by '{self.tokens.actual}' instead of ';'")

        elif self.tokens.actual.tokenType == TokenTypes.SEPARATOR:
            logger.debug(f"[ParseCommand] Consumed separator '{self.tokens.actual}'")

            ret = NoOp(value=self.tokens.actual.value)

        elif self.tokens.actual.tokenType == TokenTypes.WHILE:
            logger.debug(f"[ParseCommand] Consumed WHILE: '{self.tokens.actual}'")

            self.tokens.selectNext()
            if self.tokens.actual.tokenType != TokenTypes.LEFT_PARENTHESIS:
                logger.critical(f"[ParseCommand] WHILE is followed by '{self.tokens.actual}' instead of '('")

            logger.trace("[ParseCommand] Creating WHILE's condition AST")
            condition: Node = self.parseOrExpr()
            logger.trace("[ParseCommand] Finished creating WHILE's condition AST")

            if self.tokens.actual.tokenType != TokenTypes.RIGHT_PARENTHESIS:
                logger.critical(f"[ParseCommand] WHILE condition is followed by '{self.tokens.actual}' instead of ')'")

            logger.trace(f"[ParseCommand] Creating WHILE's command AST...")
            self.tokens.selectNext()
            command: Node = self.parseCommand()
            logger.trace(f"[ParseCommand] Finished creating WHILE's command AST. Result is:\n{command}")

            if self.tokens.actual.tokenType != TokenTypes.RIGHT_BRACKET:
                logger.critical(f"[ParseCommand] WHILE's command is followed by '{self.tokens.actual}' instead of 'RIGHT_BRACKET'")

            ret = While(Token("while", TokenTypes.WHILE), command, condition)

        elif self.tokens.actual.tokenType == TokenTypes.IF:
            logger.debug(f"[ParseCommand] Consumed IF '{self.tokens.actual}'")

            self.tokens.selectNext()
            if self.tokens.actual.tokenType != TokenTypes.LEFT_PARENTHESIS:
                logger.critical(f"[ParseCommand] IF is followed by '{self.tokens.actual}' instead of '('")

            logger.trace(f"[ParseCommand] Creating IF's condition AST...")
            condition: Node = self.parseOrExpr()
            logger.trace(f"[ParseCommand] Finished creatings IF's condition AST...")

            if self.tokens.actual.tokenType != TokenTypes.RIGHT_PARENTHESIS:
                logger.critical(f"[ParseCommand] IF's condition is followed by '{self.tokens.actual}' instead of ')'")

            logger.trace(f"[ParseCommand] Creating IF true AST...")
            self.tokens.selectNext()
            command: Node = self.parseCommand()
            logger.trace(f"[ParseCommand] Finished creating IF true AST. Result is:\n{command}")

            self.tokens.selectNext()
            if self.tokens.actual.tokenType == TokenTypes.ELSE:
                logger.debug(f"[ParseCommand] IF contains ELSE...")
                self.tokens.selectNext()
                ret = If(value=Token("if", TokenTypes.IF), ifTrue=command, ifFalse=self.parseCommand(), condition=condition)
                logger.debug(f"[ParseCommand] Finished creating ELSE's AST...")
            else:
                logger.debug(f"[ParseCommand] IF does not contain ELSE...")
                ret = If(value=Token("if", TokenTypes.IF), ifTrue=command, condition=condition)
                self.tokens.position -= len(self.tokens.actual.value)

        else:
            logger.debug(f"[ParseCommand] Consuming block in ParseCommand...")
            ret = self.parseBlock()
            logger.debug(f"[ParseCommand] Finished consuming block in ParseCommand...")

        logger.success(f"[ParseCommand] End. Result:\n{ret}")
        return ret

    def parseOrExpr(self) -> Node:
        logger.info(f"[ParseOrExpr] Start...")

        expr: Node = self.parseAndExpr()

        if self.tokens.actual.tokenType == TokenTypes.CMP_OR:
            logger.trace(f"[ParseOrExpr] Consumed OR comparison: {self.tokens.actual}")
            cmp = Comparison(self.tokens.actual, expr, self.parseAndExpr())

            while self.tokens.actual.tokenType == TokenTypes.CMP_OR:
                logger.trace(f"[ParseOrExpr] Consumed another OR comparison: {self.tokens.actual}")
                cmp = Comparison(self.tokens.actual, cmp, self.parseAndExpr())

            logger.info(f"[ParseOrExpr] Returning comparison")
            return cmp
        else:
            logger.info(f"[ParseOrExpr] No comparison, returning expression")
            return expr

    def parseAndExpr(self) -> Node:
        logger.info(f"[ParseAndExpr] Start...")

        expr: Node = self.parseEqExpr()

        if self.tokens.actual.tokenType == TokenTypes.CMP_AND:
            logger.trace(f"[ParseAndExpr] Consumed AND comparison: {self.tokens.actual}")
            cmp = Comparison(self.tokens.actual, expr, self.parseEqExpr())

            while self.tokens.actual.tokenType == TokenTypes.CMP_AND:
                logger.trace(f"[ParseAndExpr] Consumed another AND comparison: {self.tokens.actual}")
                cmp = Comparison(self.tokens.actual, cmp, self.parseEqExpr())

            logger.info(f"[ParseAndExpr] Returning comparison")
            return cmp
        else:
            logger.info(f"[ParseAndExpr] No comparison, returning expression")
            return expr

    def parseEqExpr(self) -> Node:
        logger.info(f"[ParseEqExpr] Start...")

        expr: Node = self.parseRelExpr()

        if self.tokens.actual.tokenType == TokenTypes.CMP_EQUAL:
            logger.trace(f"[ParseEqExpr] Consumed EQUALS comparison: {self.tokens.actual}")
            cmp = Comparison(self.tokens.actual, expr, self.parseRelExpr())

            while self.tokens.actual.tokenType == TokenTypes.CMP_EQUAL:
                logger.trace(f"[ParseEqExpr] Consumed another EQUALS comparison: {self.tokens.actual}")
                cmp = Comparison(self.tokens.actual, cmp, self.parseRelExpr())

            logger.info(f"[ParseEqExpr] Returning comparison")
            return cmp
        else:
            logger.info(f"[ParseEqExpr] No comparison, returning expression")
            return expr

    def parseRelExpr(self) -> Node:
        logger.info(f"[ParseRelExpr] Start...")

        expr: Node = self.parseExpression()

        if self.tokens.actual.tokenType in [TokenTypes.CMP_GREATER, TokenTypes.CMP_LESS]:
            logger.trace(f"[ParseRelExpr] Consumed GREATER|LESS comparison: {self.tokens.actual}")
            cmp = Comparison(self.tokens.actual, expr, self.parseExpression())

            while self.tokens.actual.tokenType in [TokenTypes.CMP_GREATER, TokenTypes.CMP_LESS]:
                logger.trace(f"[ParseRelExpr] Consumed another GREATER|LESS comparison: {self.tokens.actual}")
                cmp = Comparison(self.tokens.actual, cmp, self.parseExpression())

            logger.info(f"[ParseRelExpr] Returning comparison")
            return cmp
        else:
            logger.info(f"[ParseRelExpr] No comparison, returning expression")
            return expr

    def parseExpression(self) -> Node:
        logger.info(f"[ParseExpression] Start...")

        result: Node = self.parseTerm()

        while self.tokens.actual.tokenType == TokenTypes.PLUS or self.tokens.actual.tokenType == TokenTypes.MINUS:
            logger.trace(f"[ParseExpression] Consumed PLUS|MINUS: {self.tokens.actual}")
            result = BinOp(value=self.tokens.actual, left=result, right=self.parseTerm())

        logger.info(f"[ParseExpression] End")
        return result

    def parseTerm(self) -> Node:
        logger.info("[ParseTerm] Start...")

        result: Node = self.parseFactor()

        self.tokens.selectNext()
        while self.tokens.actual.tokenType == TokenTypes.MULTIPLY or self.tokens.actual.tokenType == TokenTypes.DIVIDE:
            logger.trace(f"[ParseTerm] Consumed MULTPLY|DIVIDE: {self.tokens.actual}")
            result = BinOp(value=self.tokens.actual, left=result, right=self.parseFactor())
            self.tokens.selectNext()

        logger.info("[ParseTerm] End")
        return result

    def parseFactor(self) -> Node:
        logger.info("[ParseFactor] Start...")

        ret: Node = NoOp(Token("", TokenTypes.EOF))

        self.tokens.selectNext()
        if self.tokens.actual.tokenType == TokenTypes.NUMBER:
            logger.debug(f"[ParseFactor] Consumed NUMBER: {self.tokens.actual}")
            ret = IntVal(value=self.tokens.actual)

        elif (
            self.tokens.actual.tokenType == TokenTypes.PLUS
            or self.tokens.actual.tokenType == TokenTypes.MINUS
            or self.tokens.actual.tokenType == TokenTypes.NOT
        ):
            logger.debug(f"[ParseFactor] Consumed PLUS/MINUS/NOT: {self.tokens.actual}")
            logger.trace("[ParseFactor] Started ParseFactor RECURSION...")
            ret = UnOp(value=self.tokens.actual, left=self.parseFactor())
            logger.trace("[ParseFactor] Ended ParseFactor RECURSION...")

        elif self.tokens.actual.tokenType == TokenTypes.LEFT_PARENTHESIS:
            logger.debug(f"[ParseFactor] Consumed LEFT_PARENTHESIS: {self.tokens.actual}")
            logger.trace("[ParseFactor] Started ParseOrExpr RECURSION...")
            ret = self.parseOrExpr()
            logger.trace("[ParseFactor] Ended ParseOrExpr RECURSION...")

        elif self.tokens.actual.tokenType == TokenTypes.IDENTIFIER:
            logger.debug(f"[ParseFactor] Consumed VARIABLE: {self.tokens.actual}")
            ret = Variable(self.tokens.actual)

        elif self.tokens.actual.tokenType == TokenTypes.READLN:
            logger.debug(f"[ParseFactor] Consumed READLN: {self.tokens.actual}")

            self.tokens.selectNext()
            if self.tokens.actual.tokenType != TokenTypes.LEFT_PARENTHESIS:
                logger.critical(f"[ParseFactor] READLN is followed by '{self.tokens.actual}' instead of '('")

            self.tokens.selectNext()
            if self.tokens.actual.tokenType != TokenTypes.RIGHT_PARENTHESIS:
                logger.critical(f"[ParseFactor] READLN's '(' is followed by '{self.tokens.actual}' instead of ')'")

            ret = Readln(Token("readln", TokenTypes.READLN))

        else:
            logger.critical(f"[ParseFactor] Unexpected token: {self.tokens.actual}")

        logger.info("[ParseFactor] End")
        return ret

    def run(self, code: str) -> None:
        preprocess: PreProcess = PreProcess()
        filteredCode: str = preprocess.filter(code)

        self.tokens = Tokenizer(filteredCode)

        logger.info(f"[Parser] [Run] Running Parser...")
        self.tokens.selectNext()
        ast: Block = self.parseBlock()

        self.tokens.selectNext()
        if self.tokens.actual.tokenType not in [TokenTypes.EOF]:
            logger.critical(f"Parser did not end on EOF. Actual: {self.tokens.actual}")

        logger.info(f"[Parser] [Run] Parser end...")
        logger.success(f"[Parser] Final AST:\n{ast}")
        ast.evaluate(symbolTable=self.symbolTable)
