from models import Token, Type
from structures.syntax_tree import ExpressionNode
from constants import Words


class TempNode(ExpressionNode):
    count: int = 0 
    number: int = 0

    def __init__(self, datatype: Type) -> None:
        super().__init__(Words.Temp, datatype)
        self.count += 1
        self.number = self.count

    def to_string(self):
        return f"temp {self.number}" 