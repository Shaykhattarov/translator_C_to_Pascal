from models.ast import ExpressionNode
from models import Token



class VariableNode(ExpressionNode):
    variable: Token

    def __init__(self, variable: Token) -> None:
        self.variable = variable