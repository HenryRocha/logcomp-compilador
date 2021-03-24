from tokenizer import Tokenizer
from tokens import TokenTypes
from logger import Logger, LogTypes
from preprocess import PreProcess


class Parser:
    OPERATORS: [TokenTypes] = [TokenTypes.PLUS, TokenTypes.MINUS, TokenTypes.MULTIPLY, TokenTypes.DIVIDE]
    MARKERS: [TokenTypes] = [TokenTypes.LEFT_PARENTHESIS, TokenTypes.RIGHT_PARENTHESIS]
    tokens: Tokenizer
    logger: Logger
    result: int

    def __init__(self, logger: Logger):
        self.logger = logger

    def blockOne(self, result: int) -> int:
        self.logger.log(LogTypes.NORMAL, f"Started block one... current total is: {result}")

        if self.tokens.actual.tokenType == TokenTypes.PLUS:
            self.logger.log(LogTypes.NORMAL, "Calling block two and adding the result...")
            result += self.blockTwo()
        elif self.tokens.actual.tokenType == TokenTypes.MINUS:
            self.logger.log(LogTypes.NORMAL, "Calling block two and subtracting the result...")
            result -= self.blockTwo()

        self.logger.log(LogTypes.NORMAL, f"Ended block one, result is: {result}")
        return int(result)

    def blockTwo(self) -> int:
        self.logger.log(LogTypes.NORMAL, "Started block two...")
        self.logger.log(LogTypes.NORMAL, "Calling block three...")
        result: int = self.blockThree()
        self.logger.log(LogTypes.NORMAL, "Ended call to block three...")

        self.tokens.selectNext()
        self.logger.log(LogTypes.NORMAL, f"Consumed operator {self.tokens.actual}")
        if (
            self.tokens.actual.tokenType not in self.OPERATORS
            and self.tokens.actual.tokenType not in self.MARKERS
            and self.tokens.actual.tokenType != TokenTypes.EOF
        ):
            self.logger.log(LogTypes.ERROR, f"Block two did not consume a operator: '{self.tokens.actual}'")

        while self.tokens.actual.tokenType == TokenTypes.MULTIPLY or self.tokens.actual.tokenType == TokenTypes.DIVIDE:
            if self.tokens.actual.tokenType == TokenTypes.MULTIPLY:
                self.logger.log(LogTypes.NORMAL, f"Consumed number: {self.tokens.actual}. Multiplying...")
                result *= self.blockThree()

            elif self.tokens.actual.tokenType == TokenTypes.DIVIDE:
                self.logger.log(LogTypes.NORMAL, f"Consumed number: {self.tokens.actual}. Dividing...")
                result /= self.blockThree()

            self.tokens.selectNext()
            self.logger.log(LogTypes.NORMAL, f"Consumed operator {self.tokens.actual}")

            self.logger.log(LogTypes.NORMAL, f"End of loop, current result is: {result}")

        self.logger.log(LogTypes.NORMAL, f"Ended block two, result is: {result}")
        return int(result)

    def blockThree(self) -> int:
        self.logger.log(LogTypes.NORMAL, "Started block three...")
        result: int = 0
        self.tokens.selectNext()

        if self.tokens.actual.tokenType == TokenTypes.NUMBER:
            self.logger.log(LogTypes.NORMAL, f"Consumed number {self.tokens.actual}")
            result = self.tokens.actual.value

        elif self.tokens.actual.tokenType == TokenTypes.PLUS:
            self.logger.log(LogTypes.NORMAL, f"Consumed plus {self.tokens.actual}")
            self.logger.log(LogTypes.NORMAL, "Started block three RECURSION...")
            result += self.blockThree()
            self.logger.log(LogTypes.NORMAL, "Ended block three RECURSION...")

        elif self.tokens.actual.tokenType == TokenTypes.MINUS:
            self.logger.log(LogTypes.NORMAL, f"Consumed minus {self.tokens.actual}")
            self.logger.log(LogTypes.NORMAL, "Started block three RECURSION...")
            result -= self.blockThree()
            self.logger.log(LogTypes.NORMAL, "Ended block three RECURSION...")

        elif self.tokens.actual.tokenType == TokenTypes.LEFT_PARENTHESIS:
            self.logger.log(LogTypes.NORMAL, f"Consumed parenthesis {self.tokens.actual}")
            self.logger.log(LogTypes.NORMAL, "Started expression RECURSION...")
            result = self.parseExpression()
            self.logger.log(LogTypes.NORMAL, "Ended expression RECURSION...")
        else:
            self.logger.log(LogTypes.ERROR, f"Unexpected token on block three: '{self.tokens.actual}'")

        self.logger.log(LogTypes.NORMAL, f"Ended block three, result is: {result}")
        return int(result)

    def parseExpression(self) -> int:
        result: int = self.blockTwo()

        while self.tokens.actual.tokenType == TokenTypes.PLUS or self.tokens.actual.tokenType == TokenTypes.MINUS:
            result = self.blockOne(result)

        return int(result)

    def run(self, code: str) -> int:
        preprocess: PreProcess = PreProcess()
        filteredCode: str = preprocess.filter(code, self.logger)

        self.tokens = Tokenizer(filteredCode, self.logger)
        return self.parseExpression()
