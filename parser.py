from tokenizer import Tokenizer
from token import TokenTypes
from logger import Logger, LogTypes


class Parser:
    tokens: Tokenizer
    logger: Logger

    def __init__(self, logger: Logger):
        self.logger = logger

    def parseExpression(self):
        self.tokens.selectNext()
        previousToken = self.tokens.actual

        if previousToken.tokenType == TokenTypes.EOF:
            self.logger.log(LogTypes.ERROR, "Empty input.")
        elif previousToken.tokenType != TokenTypes.NUMBER:
            self.logger.log(LogTypes.ERROR, "First token is not a number.")
        else:
            result = int(previousToken.value)

        while self.tokens.actual.tokenType != TokenTypes.EOF:
            self.tokens.selectNext()

            if self.tokens.actual.tokenType == previousToken.tokenType:
                self.logger.log(LogTypes.ERROR, "Duplicate token found.")

            if self.tokens.actual.tokenType == TokenTypes.NUMBER:
                if previousToken.tokenType == TokenTypes.PLUS:
                    result += int(self.tokens.actual.value)
                elif previousToken.tokenType == TokenTypes.MINUS:
                    result -= int(self.tokens.actual.value)
            elif self.tokens.actual.tokenType == TokenTypes.EOF and previousToken.tokenType != TokenTypes.NUMBER:
                self.logger.log(LogTypes.ERROR, "Last token is not a number.")

            previousToken = self.tokens.actual

        return result

    def run(self, code: str):
        self.tokens = Tokenizer(code, self.logger)
        return self.parseExpression()
