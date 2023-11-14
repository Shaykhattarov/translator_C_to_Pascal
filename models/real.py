from models.token import Token
from constants.tag import Tag

class Real(Token):
    value: float 

    def __init__(self, v: float):
        super().__init__(Tag.REAL)
        self.value = v

    def to_string(self):
        return str(self.value)