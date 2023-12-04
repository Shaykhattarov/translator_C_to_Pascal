from models.ast import ExpressionNode
from models import Token

class BinOpeartionNode(ExpressionNode):
    operator: Token
    left: ExpressionNode
    right: ExpressionNode

    def __init__(self, operator: Token, left: ExpressionNode, right: ExpressionNode) -> None:
        self.operator = operator
        self.left = left
        self.right = right



