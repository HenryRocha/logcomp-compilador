from abc import ABC, abstractmethod
from tokens import Token, TokenTypes


class Node(ABC):
    value: Token
    children: []

    def __init__(self, value: Token, left: Token = None, right: Token = None):
        self.value = value
        self.children = [left, right]

    @abstractmethod
    def evaluate(self) -> int:
        return 0

    def setLeftChild(self, newChild: Token) -> None:
        self.children[0] = newChild

    def setRightChild(self, newChild: Token) -> None:
        self.children[1] = newChild

    def __str__(self):
        return f"{self.value}"


class BinOp(Node):
    def __init__(self, value: Token, left: Token = None, right: Token = None):
        super().__init__(value=value, left=left, right=right)

    def evaluate(self) -> int:
        if self.value.tokenType == TokenTypes.PLUS:
            return self.children[0].evaluate() + self.children[1].evaluate()
        elif self.value.tokenType == TokenTypes.MINUS:
            return self.children[0].evaluate() - self.children[1].evaluate()
        elif self.value.tokenType == TokenTypes.MULTIPLY:
            return self.children[0].evaluate() * self.children[1].evaluate()
        elif self.value.tokenType == TokenTypes.DIVIDE:
            return self.children[0].evaluate() / self.children[1].evaluate()


class UnOp(Node):
    def __init__(self, value: Token, left: Token):
        super().__init__(value=value, left=left)

    def evaluate(self) -> int:
        if self.value.tokenType == TokenTypes.PLUS:
            return +self.children[0].evaluate()
        elif self.value.tokenType == TokenTypes.MINUS:
            return -self.children[0].evaluate()


class IntVal(Node):
    def __init__(self, value: Token):
        super().__init__(value=value)

    def evaluate(self) -> int:
        return int(self.value.value)


class NoOp(Node):
    def __init__(self, value: Token):
        super().__init__(value=value)

    def evaluate(self) -> int:
        return 0
