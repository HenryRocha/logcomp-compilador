from tokenizer import Tokenizer
from token import TokenTypes
from logger import Logger, LogTypes


class Parser:
    tokens: Tokenizer
    logger: Logger
    result: float

    def __init__(self, logger: Logger):
        self.logger = logger

    def blockOne(self, result: float):
        self.logger.log(LogTypes.NORMAL, "Started block one...")

        if self.tokens.actual.tokenType == TokenTypes.PLUS:
            self.logger.log(LogTypes.NORMAL, "Calling block two and adding the result...")
            result += self.blockTwo()
        elif self.tokens.actual.tokenType == TokenTypes.MINUS:
            self.logger.log(LogTypes.NORMAL, "Calling block two and subtracting the result...")
            result -= self.blockTwo()

        self.logger.log(LogTypes.NORMAL, f"Ended block one, result is: {result}")
        return result

    def blockTwo(self):
        self.logger.log(LogTypes.NORMAL, "Started block two...")

        self.tokens.selectNext()
        self.logger.log(LogTypes.NORMAL, f"Consumed number: {self.tokens.actual}")
        result: float = float(self.tokens.actual.value)

        self.tokens.selectNext()
        self.logger.log(LogTypes.NORMAL, f"Consumed operator {self.tokens.actual}")

        while self.tokens.actual.tokenType == TokenTypes.MULTIPLY or self.tokens.actual.tokenType == TokenTypes.DIVIDE:
            if self.tokens.actual.tokenType == TokenTypes.MULTIPLY:
                self.tokens.selectNext()
                self.logger.log(LogTypes.NORMAL, f"Consumed number: {self.tokens.actual}. Multiplying...")
                result *= float(self.tokens.actual.value)
            elif self.tokens.actual.tokenType == TokenTypes.DIVIDE:
                self.tokens.selectNext()
                self.logger.log(LogTypes.NORMAL, f"Consumed number: {self.tokens.actual}. Dividing...")
                result /= float(self.tokens.actual.value)

            self.tokens.selectNext()
            self.logger.log(LogTypes.NORMAL, f"Consumed operator {self.tokens.actual}")

            self.logger.log(LogTypes.NORMAL, f"End of loop, current result is: {result}")

        self.logger.log(LogTypes.NORMAL, f"Ended block two, result is: {result}")
        return result

    def parseExpression(self):
        result: float = self.blockTwo()

        while self.tokens.actual.tokenType != TokenTypes.EOF:
            result = self.blockOne(result)

        return result

    def run(self, code: str):
        self.tokens = Tokenizer(code, self.logger)
        return self.parseExpression()
