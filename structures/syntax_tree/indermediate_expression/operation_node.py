from models import *
from models import Token, Type
from structures.syntax_tree import ExpressionNode, TempNode


class OperationNode(ExpressionNode):

    def __init__(self, token: Token, datatype: Type) -> None:
        super().__init__(token, datatype)

    def reduce(self):
        expression = ExpressionNode.generate()
        temp = TempNode(Type)
        return temp