from logger import Logger, LogTypes
from node import Node, BinOp, UnOp, IntVal, NoOp, Identifier, Print, Readln, Comparison, If, Block, Variable, While
from preprocess import PreProcess
from tokenizer import Tokenizer
from tokens import Token, TokenTypes
from symbolTable import SymbolTable


class Parser:
    OPERATORS: [TokenTypes] = [TokenTypes.PLUS, TokenTypes.MINUS, TokenTypes.MULTIPLY, TokenTypes.DIVIDE]
    MARKERS: [TokenTypes] = [TokenTypes.LEFT_PARENTHESIS, TokenTypes.RIGHT_PARENTHESIS, TokenTypes.SEPARATOR]
    CMPS: [TokenTypes] = [TokenTypes.CMP_EQUAL, TokenTypes.CMP_GREATER, TokenTypes.CMP_LESS, TokenTypes.CMP_AND, TokenTypes.CMP_OR]
    tokens: Tokenizer
    logger: Logger
    symbolTable: SymbolTable
    result: int

    def __init__(self, logger: Logger):
        self.logger = logger
        self.symbolTable = SymbolTable(self.logger)

    def parseBlock(self) -> Node:
        self.logger.log(LogTypes.NORMAL, f"Started ParseBlock...")

        ret: Node = Block()

        if self.tokens.actual.tokenType != TokenTypes.LEFT_BRACKET:
            self.logger.log(LogTypes.ERROR, f"Block cannot start with {self.tokens.actual}")

        self.tokens.selectNext()
        while self.tokens.actual.tokenType != TokenTypes.RIGHT_BRACKET:
            ret.addNode(self.parseCommand())
            self.tokens.selectNext()

        if self.tokens.actual.tokenType != TokenTypes.RIGHT_BRACKET:
            self.logger.log(LogTypes.ERROR, f"Block cannot end with {self.tokens.actual}")

        self.logger.log(LogTypes.NORMAL, f"Ended ParseBlock...")
        return ret

    def parseCommand(self) -> Node:
        self.logger.log(LogTypes.NORMAL, f"Started ParseCommand...")

        ret: Node = None

        if self.tokens.actual.tokenType == TokenTypes.IDENTIFIER:
            self.logger.log(LogTypes.NORMAL, f"Consumed identifier '{self.tokens.actual}'")
            variableName: str = self.tokens.actual.value

            self.tokens.selectNext()
            if self.tokens.actual.tokenType != TokenTypes.ASSIGN:
                self.logger.log(LogTypes.ERROR, f"Identifier is followed by '{self.tokens.actual}' instead of '='")

            self.logger.log(LogTypes.NORMAL, f"Calling ParseOrExpr to create the variable's AST...")
            ret = Identifier(value=variableName, left=self.parseOrExpr())
            self.logger.log(LogTypes.NORMAL, f"Finished creating variable's AST (ended call to ParseOrExpr)")

            if self.tokens.actual.tokenType != TokenTypes.SEPARATOR:
                self.logger.log(LogTypes.ERROR, f"Assign expression is followed by '{self.tokens.actual}' instead of ';'")

        elif self.tokens.actual.tokenType == TokenTypes.PRINT:
            self.logger.log(LogTypes.NORMAL, f"Consumed println '{self.tokens.actual}'")

            self.tokens.selectNext()
            if self.tokens.actual.tokenType != TokenTypes.LEFT_PARENTHESIS:
                self.logger.log(LogTypes.ERROR, f"Println is followed by '{self.tokens.actual}' instead of '('")

            self.logger.log(LogTypes.NORMAL, f"Calling ParseOrExpr to create Println's AST...")
            ret = Print(value=self.tokens.actual.value, left=self.parseOrExpr())
            self.logger.log(LogTypes.NORMAL, f"Finished creating println's AST (ended call to ParseOrExpr)")

            if self.tokens.actual.tokenType != TokenTypes.RIGHT_PARENTHESIS:
                self.logger.log(LogTypes.ERROR, f"Println expression is followed by '{self.tokens.actual}' instead of ')'")

            self.tokens.selectNext()
            if self.tokens.actual.tokenType != TokenTypes.SEPARATOR:
                self.logger.log(LogTypes.ERROR, f"Println ')' is followed by '{self.tokens.actual}' instead of ';'")

        elif self.tokens.actual.tokenType == TokenTypes.SEPARATOR:
            self.logger.log(LogTypes.NORMAL, f"Consumed separator '{self.tokens.actual}'")

            ret = NoOp(value=self.tokens.actual.value)

        elif self.tokens.actual.tokenType == TokenTypes.WHILE:
            self.logger.log(LogTypes.NORMAL, f"Consumed WHILE '{self.tokens.actual}'")

            self.tokens.selectNext()
            if self.tokens.actual.tokenType != TokenTypes.LEFT_PARENTHESIS:
                self.logger.log(LogTypes.ERROR, f"Token WHILE is followed by '{self.tokens.actual}' instead of '('")

            self.logger.log(LogTypes.NORMAL, f"Calling ParseOrExpr to create WHILE's condition...")
            condition: Node = self.parseOrExpr()
            self.logger.log(LogTypes.NORMAL, f"Finished creating WHILE's condition (ended call to ParseOrExpr)")

            if self.tokens.actual.tokenType != TokenTypes.RIGHT_PARENTHESIS:
                self.logger.log(LogTypes.ERROR, f"Token WHILE condition is followed by '{self.tokens.actual}' instead of ')'")

            self.logger.log(LogTypes.NORMAL, f"Consuming WHILE's command...")
            self.tokens.selectNext()
            command: Node = self.parseCommand()
            self.logger.log(LogTypes.NORMAL, f"Finished consuming WHILE's command...")
            self.logger.log(LogTypes.NORMAL, f"WHILE's command is: {type(command)}")

            ret = While(Token("while", TokenTypes.WHILE), command, condition)

        elif self.tokens.actual.tokenType == TokenTypes.IF:
            self.logger.log(LogTypes.NORMAL, f"Consumed IF '{self.tokens.actual}'")

            self.tokens.selectNext()
            if self.tokens.actual.tokenType != TokenTypes.LEFT_PARENTHESIS:
                self.logger.log(LogTypes.ERROR, f"Token IF is followed by '{self.tokens.actual}' instead of '('")

            self.logger.log(LogTypes.NORMAL, f"Calling ParseOrExpr to create IF's condition AST...")
            condition: Node = self.parseOrExpr()
            self.logger.log(LogTypes.NORMAL, f"Finished creating IF's condition AST (ended call to ParseOrExpr)...")

            if self.tokens.actual.tokenType != TokenTypes.RIGHT_PARENTHESIS:
                self.logger.log(LogTypes.ERROR, f"Token IF condition is followed by '{self.tokens.actual}' instead of ')'")

            self.logger.log(LogTypes.NORMAL, f"Consuming IF's command...")
            self.tokens.selectNext()
            command: Node = self.parseCommand()
            self.logger.log(LogTypes.NORMAL, f"Finished consuming IF's command...")
            self.logger.log(LogTypes.NORMAL, f"IF's command is: {type(command)}. Current token is: {self.tokens.actual}")

            self.tokens.selectNext()
            if self.tokens.actual.tokenType == TokenTypes.ELSE:
                self.logger.log(LogTypes.NORMAL, f"IF contains ELSE...")
                self.tokens.selectNext()
                ret = If(value=Token("if", TokenTypes.IF), ifTrue=command, ifFalse=self.parseCommand(), condition=condition)
            else:
                self.logger.log(LogTypes.NORMAL, f"IF does not contain ELSE...")
                ret = If(value=Token("if", TokenTypes.IF), ifTrue=command, condition=condition)
                self.tokens.position -= len(self.tokens.actual.value)

        elif self.tokens.actual.tokenType == TokenTypes.LEFT_BRACKET:
            self.logger.log(LogTypes.NORMAL, f"Consuming block in ParseCommand...")
            ret = self.parseBlock()
            self.logger.log(LogTypes.NORMAL, f"Finished consuming block in ParseCommand...")

        else:
            self.logger.log(LogTypes.ERROR, f"Unexpected token in ParseCommand: {self.tokens.actual}...")

        self.logger.log(LogTypes.NORMAL, f"Ended ParseCommand...")
        return ret

    def parseOrExpr(self) -> Node:
        self.logger.log(LogTypes.NORMAL, f"Started ParseOrExpr...")

        self.logger.log(LogTypes.NORMAL, "Calling ParseAndExpr...")
        expr: Node = self.parseAndExpr()
        self.logger.log(LogTypes.NORMAL, "Ended call to ParseAndExpr...")

        if self.tokens.actual.tokenType == TokenTypes.CMP_OR:
            self.logger.log(LogTypes.NORMAL, f"Consumed comparison: {self.tokens.actual}")
            cmp = Comparison(self.tokens.actual, expr, self.parseAndExpr())

            while self.tokens.actual.tokenType == TokenTypes.CMP_OR:
                self.logger.log(LogTypes.NORMAL, f"Consumed another comparison: {self.tokens.actual}")
                cmp = Comparison(self.tokens.actual, cmp, self.parseAndExpr())

            return cmp
        else:
            self.logger.log(LogTypes.NORMAL, f"No comparison, returning expression: {expr}")
            return expr

    def parseAndExpr(self) -> Node:
        self.logger.log(LogTypes.NORMAL, f"Started ParseAndExpr...")

        self.logger.log(LogTypes.NORMAL, "Calling ParseEqExpr...")
        expr: Node = self.parseEqExpr()
        self.logger.log(LogTypes.NORMAL, "Ended call to ParseEqExpr...")

        if self.tokens.actual.tokenType == TokenTypes.CMP_AND:
            self.logger.log(LogTypes.NORMAL, f"Consumed comparison: {self.tokens.actual}")
            cmp = Comparison(self.tokens.actual, expr, self.parseEqExpr())

            while self.tokens.actual.tokenType == TokenTypes.CMP_AND:
                self.logger.log(LogTypes.NORMAL, f"Consumed another comparison: {self.tokens.actual}")
                cmp = Comparison(self.tokens.actual, cmp, self.parseEqExpr())

            return cmp
        else:
            self.logger.log(LogTypes.NORMAL, f"No comparison, returning expression: {expr}")
            return expr

    def parseEqExpr(self) -> Node:
        self.logger.log(LogTypes.NORMAL, f"Started ParseEqExpr...")

        self.logger.log(LogTypes.NORMAL, "Calling ParseRelExpr...")
        expr: Node = self.parseRelExpr()
        self.logger.log(LogTypes.NORMAL, "Ended call to ParseRelExpr...")

        if self.tokens.actual.tokenType == TokenTypes.CMP_EQUAL:
            self.logger.log(LogTypes.NORMAL, f"Consumed comparison: {self.tokens.actual}")
            cmp = Comparison(self.tokens.actual, expr, self.parseRelExpr())

            while self.tokens.actual.tokenType == TokenTypes.CMP_EQUAL:
                self.logger.log(LogTypes.NORMAL, f"Consumed another comparison: {self.tokens.actual}")
                cmp = Comparison(self.tokens.actual, cmp, self.parseRelExpr())

            return cmp
        else:
            self.logger.log(LogTypes.NORMAL, f"No comparison, returning expression: {expr}")
            return expr

    def parseRelExpr(self) -> Node:
        self.logger.log(LogTypes.NORMAL, f"Started ParseRelExpr...")

        self.logger.log(LogTypes.NORMAL, "Calling ParseExpression...")
        expr: Node = self.parseExpression()
        self.logger.log(LogTypes.NORMAL, "Ended call to ParseExpression...")

        if self.tokens.actual.tokenType in [TokenTypes.CMP_GREATER, TokenTypes.CMP_LESS]:
            self.logger.log(LogTypes.NORMAL, f"Consumed comparison: {self.tokens.actual}")
            cmp = Comparison(self.tokens.actual, expr, self.parseExpression())

            while self.tokens.actual.tokenType in [TokenTypes.CMP_GREATER, TokenTypes.CMP_LESS]:
                self.logger.log(LogTypes.NORMAL, f"Consumed another comparison: {self.tokens.actual}")
                cmp = Comparison(self.tokens.actual, cmp, self.parseExpression())

            return cmp
        else:
            self.logger.log(LogTypes.NORMAL, f"No comparison, returning expression: {expr}")
            return expr

    def parseExpression(self) -> Node:
        self.logger.log(LogTypes.NORMAL, f"Started ParseExpression...")
        result: Node = self.parseTerm()

        while self.tokens.actual.tokenType == TokenTypes.PLUS or self.tokens.actual.tokenType == TokenTypes.MINUS:
            self.logger.log(LogTypes.NORMAL, "Calling ParseTerm to add/subtract...")
            result = BinOp(value=self.tokens.actual, left=result, right=self.parseTerm())

        self.logger.log(LogTypes.NORMAL, f"Ended ParseExpression...")
        return result

    def parseTerm(self) -> Node:
        self.logger.log(LogTypes.NORMAL, "Started ParseTerm...")
        result: Node = self.parseFactor()

        self.tokens.selectNext()
        while self.tokens.actual.tokenType == TokenTypes.MULTIPLY or self.tokens.actual.tokenType == TokenTypes.DIVIDE:
            self.logger.log(LogTypes.NORMAL, f"Calling ParseFactor to multiply/divide...")
            result = BinOp(value=self.tokens.actual, left=result, right=self.parseFactor())
            self.tokens.selectNext()

        self.logger.log(LogTypes.NORMAL, "Ended ParseTerm...")
        return result

    def parseFactor(self) -> Node:
        self.logger.log(LogTypes.NORMAL, "Started ParseFactor...")

        ret: Node = None

        self.tokens.selectNext()
        if self.tokens.actual.tokenType == TokenTypes.NUMBER:
            self.logger.log(LogTypes.NORMAL, f"Consumed number {self.tokens.actual}")
            ret: IntVal = IntVal(value=self.tokens.actual)

        elif (
            self.tokens.actual.tokenType == TokenTypes.PLUS
            or self.tokens.actual.tokenType == TokenTypes.MINUS
            or self.tokens.actual.tokenType == TokenTypes.NOT
        ):
            self.logger.log(LogTypes.NORMAL, f"Consumed plus/minus/not {self.tokens.actual}")
            self.logger.log(LogTypes.NORMAL, "Started ParseFactor RECURSION...")
            ret: UnOp = UnOp(value=self.tokens.actual, left=self.parseFactor())
            self.logger.log(LogTypes.NORMAL, "Ended ParseFactor RECURSION...")

        elif self.tokens.actual.tokenType == TokenTypes.LEFT_PARENTHESIS:
            self.logger.log(LogTypes.NORMAL, f"Consumed parenthesis EXPRESSION {self.tokens.actual}")
            self.logger.log(LogTypes.NORMAL, "Started ParseOrExpr...")
            ret: Node = self.parseOrExpr()
            self.logger.log(LogTypes.NORMAL, "Ended ParseOrExpr...")

        elif self.tokens.actual.tokenType == TokenTypes.IDENTIFIER:
            self.logger.log(LogTypes.NORMAL, f"Consumed variable lookup {self.tokens.actual}")
            ret: Node = Variable(self.tokens.actual)

        elif self.tokens.actual.tokenType == TokenTypes.READLN:
            self.logger.log(LogTypes.NORMAL, f"Consumed READLN {self.tokens.actual}")

            self.tokens.selectNext()
            if self.tokens.actual.tokenType != TokenTypes.LEFT_PARENTHESIS:
                self.logger.log(LogTypes.ERROR, f"Unexpected token after READLN: {self.tokens.actual}")

            self.tokens.selectNext()
            if self.tokens.actual.tokenType != TokenTypes.RIGHT_PARENTHESIS:
                self.logger.log(LogTypes.ERROR, f"Unexpected token after READLN's left parenthesis: {self.tokens.actual}")

        self.logger.log(LogTypes.NORMAL, "Ended ParseFactor...")
        return ret

    def run(self, code: str) -> None:
        preprocess: PreProcess = PreProcess()
        filteredCode: str = preprocess.filter(code, self.logger)

        self.tokens = Tokenizer(filteredCode, self.logger)

        self.tokens.selectNext()
        self.parseBlock().evaluate(symbolTable=self.symbolTable, logger=self.logger)
