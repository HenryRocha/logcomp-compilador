from tokenizer import Tokenizer
from token import TokenTypes
from logger import Logger, LogTypes


class Parser:
    OPERATORS: [TokenTypes] = [TokenTypes.PLUS, TokenTypes.MINUS, TokenTypes.MULTIPLY, TokenTypes.DIVIDE]
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

        if self.tokens.actual.tokenType != TokenTypes.NUMBER:
            self.logger.log(LogTypes.ERROR, "First token in current expression is not a number.")
        else:
            result: float = float(self.tokens.actual.value)

        self.tokens.selectNext()
        self.logger.log(LogTypes.NORMAL, f"Consumed operator {self.tokens.actual}")

        if self.tokens.actual.tokenType not in self.OPERATORS and self.tokens.actual.tokenType != TokenTypes.EOF:
            self.logger.log(LogTypes.ERROR, "Second token is not an operator.")

        while self.tokens.actual.tokenType == TokenTypes.MULTIPLY or self.tokens.actual.tokenType == TokenTypes.DIVIDE:
            if self.tokens.actual.tokenType == TokenTypes.MULTIPLY:
                self.tokens.selectNext()
                if self.tokens.actual.tokenType in self.OPERATORS:
                    self.logger.log(LogTypes.ERROR, "Two operators in a row.")
                elif self.tokens.actual.tokenType == TokenTypes.EOF:
                    self.logger.log(LogTypes.ERROR, "Ending operator is '*'.")

                self.logger.log(LogTypes.NORMAL, f"Consumed number: {self.tokens.actual}. Multiplying...")
                result *= float(self.tokens.actual.value)
            elif self.tokens.actual.tokenType == TokenTypes.DIVIDE:
                self.tokens.selectNext()
                if self.tokens.actual.tokenType in self.OPERATORS:
                    self.logger.log(LogTypes.ERROR, "Two operators in a row.")
                elif self.tokens.actual.tokenType == TokenTypes.EOF:
                    self.logger.log(LogTypes.ERROR, "Ending operator is '/'.")

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
