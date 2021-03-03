from token_types import TokenTypes


class Token:
    tokenType: TokenTypes
    value: str

    def __init__(self, value: str, tokenType: TokenTypes):
        self.tokenType = tokenType
        self.value = value
