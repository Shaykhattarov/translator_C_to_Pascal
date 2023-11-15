from models.token import Token
from constants.tag import Tag

class Float(Token):
    value: float 

    def __init__(self, v: float):
        super().__init__(Tag.FLOAT)
        self.value = v

    def to_string(self):
        return str(self.value)
    
    def __repr__(self) -> str:
        return f"<Float {self.value} - {self.tag} - {self.length}>"