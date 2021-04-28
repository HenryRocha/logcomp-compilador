from logger import Logger, LogTypes
from node import Node, BinOp, UnOp, IntVal, NoOp, Identifier, Print
from preprocess import PreProcess
from tokenizer import Tokenizer
from tokens import Token, TokenTypes
from symbolTable import SymbolTable


class Parser:
    OPERATORS: [TokenTypes] = [TokenTypes.PLUS, TokenTypes.MINUS, TokenTypes.MULTIPLY, TokenTypes.DIVIDE]
    MARKERS: [TokenTypes] = [TokenTypes.LEFT_PARENTHESIS, TokenTypes.RIGHT_PARENTHESIS, TokenTypes.SEPARATOR]
    tokens: Tokenizer
    logger: Logger
    symbolTable: SymbolTable
    result: int

    def __init__(self, logger: Logger):
        self.logger = logger
        self.symbolTable = SymbolTable(self.logger)

    def blockOne(self, result: Node) -> Node:
        self.logger.log(LogTypes.NORMAL, f"Started block one... current total is: {result}")

        if self.tokens.actual.tokenType == TokenTypes.PLUS:
            self.logger.log(LogTypes.NORMAL, "Calling block two and adding the result...")
            result = BinOp(value=self.tokens.actual, left=result, right=self.blockTwo())
        elif self.tokens.actual.tokenType == TokenTypes.MINUS:
            self.logger.log(LogTypes.NORMAL, "Calling block two and subtracting the result...")
            result = BinOp(value=self.tokens.actual, left=result, right=self.blockTwo())

        self.logger.log(LogTypes.NORMAL, f"Ended block one, result is: {result}")
        return result

    def blockTwo(self) -> Node:
        self.logger.log(LogTypes.NORMAL, "Started block two...")
        self.logger.log(LogTypes.NORMAL, "Calling block three...")
        result: Node = self.blockThree()
        self.logger.log(LogTypes.NORMAL, "Ended call to block three...")

        self.tokens.selectNext()
        self.logger.log(LogTypes.NORMAL, f"Consumed operator {self.tokens.actual}")
        if (
            self.tokens.actual.tokenType not in self.OPERATORS
            and self.tokens.actual.tokenType not in self.MARKERS
            and self.tokens.actual.tokenType != TokenTypes.EOF
        ):
            self.logger.log(LogTypes.ERROR, f"Block two did not consume a operator: '{self.tokens.actual}'")
        elif self.tokens.actual.tokenType == TokenTypes.LEFT_PARENTHESIS and type(result) == IntVal:
            self.logger.log(LogTypes.ERROR, f"Block two found unexpected parenthesis: '{self.tokens.actual}'")

        while self.tokens.actual.tokenType == TokenTypes.MULTIPLY or self.tokens.actual.tokenType == TokenTypes.DIVIDE:
            if self.tokens.actual.tokenType == TokenTypes.MULTIPLY or self.tokens.actual.tokenType == TokenTypes.DIVIDE:
                self.logger.log(LogTypes.NORMAL, f"Consumed number: {self.tokens.actual}. Multiplying/dividing...")
                result = BinOp(value=self.tokens.actual, left=result, right=self.blockThree())

            self.tokens.selectNext()
            self.logger.log(LogTypes.NORMAL, f"Consumed operator {self.tokens.actual}")

            self.logger.log(LogTypes.NORMAL, f"End of loop, current result is: {result}")

        self.logger.log(LogTypes.NORMAL, f"Ended block two, result is: {result}")
        return result

    def blockThree(self) -> Node:
        self.logger.log(LogTypes.NORMAL, "Started block three...")

        self.tokens.selectNext()
        if self.tokens.actual.tokenType == TokenTypes.NUMBER:
            self.logger.log(LogTypes.NORMAL, f"Consumed number {self.tokens.actual}")
            ret: IntVal = IntVal(value=self.tokens.actual)
            self.logger.log(LogTypes.NORMAL, f"Ended block three, result is: {ret}")
            return ret

        elif self.tokens.actual.tokenType == TokenTypes.PLUS or self.tokens.actual.tokenType == TokenTypes.MINUS:
            self.logger.log(LogTypes.NORMAL, f"Consumed plus/minus {self.tokens.actual}")
            self.logger.log(LogTypes.NORMAL, "Started block three RECURSION...")
            ret: UnOp = UnOp(value=self.tokens.actual, left=self.blockThree())
            self.logger.log(LogTypes.NORMAL, "Ended block three RECURSION...")
            self.logger.log(LogTypes.NORMAL, f"Ended block three, result is: {ret}")
            return ret

        elif self.tokens.actual.tokenType == TokenTypes.LEFT_PARENTHESIS:
            self.logger.log(LogTypes.NORMAL, f"Consumed parenthesis {self.tokens.actual}")
            self.logger.log(LogTypes.NORMAL, "Started expression RECURSION...")
            ret: Node = self.parseExpression()
            self.logger.log(LogTypes.NORMAL, "Ended expression RECURSION...")
            self.logger.log(LogTypes.NORMAL, f"Ended block three, result is: {ret}")
            return ret

        elif self.tokens.actual.tokenType == TokenTypes.IDENTIFIER:
            self.logger.log(LogTypes.NORMAL, f"Consumed identifier {self.tokens.actual}")
            ret: Node = self.symbolTable.getVar(self.tokens.actual.value)
            self.logger.log(LogTypes.NORMAL, f"Ended block three, result is: {ret}")
            return ret

        else:
            self.logger.log(LogTypes.ERROR, f"Unexpected token on block three: '{self.tokens.actual}'")

    def parseBlock(self) -> None:
        self.logger.log(LogTypes.NORMAL, f"Started ParseBlock...")

        self.tokens.selectNext()
        while self.tokens.actual.tokenType != TokenTypes.EOF:
            statement: Node = self.parseCommand()
            statement.evaluate(symbolTable=self.symbolTable)
            self.tokens.selectNext()

        self.logger.log(LogTypes.NORMAL, f"Ended ParseBlock...")

    def parseCommand(self) -> Node:
        self.logger.log(LogTypes.NORMAL, f"Started ParseCommand...")

        ret: Node = None

        if self.tokens.actual.tokenType == TokenTypes.IDENTIFIER:
            self.logger.log(LogTypes.NORMAL, f"Consumed identifier '{self.tokens.actual}'")
            variableName: str = self.tokens.actual.value

            self.tokens.selectNext()
            if self.tokens.actual.tokenType != TokenTypes.ASSIGN:
                self.logger.log(LogTypes.ERROR, f"Identifier is followed by '{self.tokens.actual}' instead of '='")

            self.logger.log(LogTypes.NORMAL, f"Calling ParseExpression to create the variable's AST...")
            ret = Identifier(value=variableName, left=self.parseExpression())
            self.logger.log(LogTypes.NORMAL, f"Ended call to ParseExpression...")

            if self.tokens.actual.tokenType != TokenTypes.SEPARATOR:
                self.logger.log(LogTypes.ERROR, f"Assign expression is followed by '{self.tokens.actual}' instead of ';'")

        elif self.tokens.actual.tokenType == TokenTypes.PRINT:
            self.logger.log(LogTypes.NORMAL, f"Consumed println '{self.tokens.actual}'")

            self.tokens.selectNext()
            if self.tokens.actual.tokenType != TokenTypes.LEFT_PARENTHESIS:
                self.logger.log(LogTypes.ERROR, f"Println is followed by '{self.tokens.actual}' instead of '('")

            self.logger.log(LogTypes.NORMAL, f"Calling ParseExpression to create Println's AST...")
            ret = Print(value=self.tokens.actual.value, left=self.parseExpression())
            self.logger.log(LogTypes.NORMAL, f"Ended call to ParseExpression...")

            if self.tokens.actual.tokenType != TokenTypes.RIGHT_PARENTHESIS:
                self.logger.log(LogTypes.ERROR, f"Println expression is followed by '{self.tokens.actual}' instead of ')'")

            self.tokens.selectNext()
            if self.tokens.actual.tokenType != TokenTypes.SEPARATOR:
                self.logger.log(LogTypes.ERROR, f"Println ')' is followed by '{self.tokens.actual}' instead of ';'")

        else:
            self.logger.log(LogTypes.ERROR, f"Command does not start with IDENTIFIER or PRINT")

        self.logger.log(LogTypes.NORMAL, f"Ended ParseCommand...")
        return ret

    def parseExpression(self) -> Node:
        result: Node = self.blockTwo()

        while self.tokens.actual.tokenType == TokenTypes.PLUS or self.tokens.actual.tokenType == TokenTypes.MINUS:
            result = self.blockOne(result)

        return result

    def run(self, code: str) -> None:
        preprocess: PreProcess = PreProcess()
        filteredCode: str = preprocess.filter(code, self.logger)

        self.tokens = Tokenizer(filteredCode, self.logger)
        self.parseBlock()
