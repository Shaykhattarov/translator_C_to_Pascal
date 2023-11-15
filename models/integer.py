from models.token import Token
from constants.tag import Tag


class Integer(Token):
    value: int

    def __init__(self, v: int):
        super().__init__(Tag.INT)
        self.value = v

    def to_string(self):
        return self.value

    def __repr__(self) -> str:
        return f"<INTEGER {self.value} - {self.tag} - {self.length}>"