from models.token import Token
from constants.tag import Tag


class Num(Token):
    value: int

    def __init__(self, v: int):
        super().__init__(Tag.NUM)
        self.value = v

    def to_string(self):
        return self.value