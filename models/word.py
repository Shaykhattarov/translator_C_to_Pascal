from models.token import Token

class Word(Token):
    lexeme: str = ""
    
    def __init__(self, s: str, tag: int):
        super().__init__(tag)
        self.lexeme = s

    def to_string(self):
        return self.lexeme
    
    def __repr__(self) -> str:
        return f"<Word {self.lexeme} - {self.tag}>"
    
    

