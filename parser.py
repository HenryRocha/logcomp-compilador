from tokenizer import Tokenizer
from token_types import TokenTypes


class Parser:
    tokens: Tokenizer

    def parseExpression(self):
        self.tokens.selectNext()
        previousToken = self.tokens.actual

        if previousToken.tokenType == TokenTypes.EOF:
            raise ValueError("Empty input.")
        elif previousToken.tokenType != TokenTypes.NUMBER:
            raise ValueError("First token is not a number.")
        else:
            result = int(previousToken.value)

        while self.tokens.actual.tokenType != TokenTypes.EOF:
            self.tokens.selectNext()

            if self.tokens.actual.tokenType == previousToken.tokenType:
                raise ValueError("Duplicate token found.")

            if self.tokens.actual.tokenType == TokenTypes.NUMBER:
                if previousToken.tokenType == TokenTypes.PLUS:
                    result += int(self.tokens.actual.value)
                elif previousToken.tokenType == TokenTypes.MINUS:
                    result -= int(self.tokens.actual.value)
            elif self.tokens.actual.tokenType == TokenTypes.EOF and previousToken.tokenType != TokenTypes.NUMBER:
                raise ValueError("Last token is not a number.")

            previousToken = self.tokens.actual

        return result

    def run(self, code: str):
        self.tokens = Tokenizer(code)
        return self.parseExpression()
