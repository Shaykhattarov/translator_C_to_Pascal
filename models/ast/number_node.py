from models.ast import ExpressionNode
from models import Token


class NumberNode(ExpressionNode):
    number: Token

    def __init__(self, number: Token) -> None:
        self.number = number

