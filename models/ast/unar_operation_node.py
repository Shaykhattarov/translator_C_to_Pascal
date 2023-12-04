from models.ast import ExpressionNode
from models import Token

class UnarOperationNode(ExpressionNode):
    operator: Token
    operand: ExpressionNode

    def __init__(self, operator: Token, operand: ExpressionNode) -> None:
        self.operator = operator
        self.operand = operand