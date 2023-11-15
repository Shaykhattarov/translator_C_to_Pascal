
class Token:
    tag: str
    length: str
    value: int = None

    def __init__(self, t: str):
        self.tag = t
        self.length = len(f"{self.tag}")
    
    def to_string(self) -> str:
        return str(self.tag)
    
    def __repr__(self) -> str:
        if self.value is not None:
            return f"<Token {self.tag} - {self.value}>"
        else:
            return f"<Token {self.tag}>"
    
