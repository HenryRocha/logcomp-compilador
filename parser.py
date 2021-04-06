from logger import Logger, LogTypes
from node import Node, BinOp, UnOp, IntVal, NoOp
from preprocess import PreProcess
from tokenizer import Tokenizer
from tokens import Token, TokenTypes


class Parser:
    OPERATORS: [TokenTypes] = [TokenTypes.PLUS, TokenTypes.MINUS, TokenTypes.MULTIPLY, TokenTypes.DIVIDE]
    MARKERS: [TokenTypes] = [TokenTypes.LEFT_PARENTHESIS, TokenTypes.RIGHT_PARENTHESIS]
    tokens: Tokenizer
    logger: Logger
    result: int

    def __init__(self, logger: Logger):
        self.logger = logger

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

        else:
            self.logger.log(LogTypes.ERROR, f"Unexpected token on block three: '{self.tokens.actual}'")

    def parseExpression(self) -> Node:
        result: Node = self.blockTwo()

        while self.tokens.actual.tokenType == TokenTypes.PLUS or self.tokens.actual.tokenType == TokenTypes.MINUS:
            result = self.blockOne(result)

        return result

    def run(self, code: str) -> int:
        preprocess: PreProcess = PreProcess()
        filteredCode: str = preprocess.filter(code, self.logger)

        self.tokens = Tokenizer(filteredCode, self.logger)
        return self.parseExpression()
