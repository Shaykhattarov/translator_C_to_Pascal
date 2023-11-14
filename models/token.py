
class Token:
    tag: int

    def __init__(self, t: int):
        self.tag = t
    
    def to_string(self) -> str:
        return str(self.tag)
    
    def __repr__(self) -> str:
        return "<Token {}>".format(self.tag)
