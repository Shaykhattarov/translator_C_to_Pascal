
class Token:
    tag: str
    length: str
    lexeme: str 

    def __init__(self, lex: str, tag: str) -> None:
        self.lexeme = lex
        self.tag = tag
        self.length = len(self.lexeme)

    def __repr__(self):
        return f"<Token {self.lexeme} - {self.tag} - {self.length}>"

    
