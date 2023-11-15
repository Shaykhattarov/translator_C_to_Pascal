from models import Token, Type, Word
from structures.syntax_tree import ExpressionNode


class IdentifierNode(ExpressionNode):
    offset: int 

    def __init__(self, id: Word, p: Type, offset: int) -> None:
        super().__init__(id, p)
        self.offset = offset