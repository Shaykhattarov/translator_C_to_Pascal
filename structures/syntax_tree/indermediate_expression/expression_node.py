from models import *
from structures.syntax_tree import SyntaxTreeNode

class ExpressionNode(SyntaxTreeNode):
    operation: Token
    datatype: Type

    def __init__(self, operation: Token, datatype: Type) -> None:
        self.operation = operation
        self.datatype = datatype

    def generate(self):
        return self
    
    def reduce(self):
        return self
    
    def to_string(self):
        return self.operation.to_string()