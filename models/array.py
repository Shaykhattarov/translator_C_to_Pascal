from models.type import Type
from constants.tag import Tag

class Array(Type):
    type: Type
    size: int = 1

    def __init__(self, size: int, type: Type):
        super().__init__("[]", Tag.INDEX, size * type.width)
        self.size = size
        self.type = type

    def to_string(self):
        return f"[{self.size}] {self.type}"
    
    def __repr__(self) -> str:
        return f"[{self.size}] {self.type}"