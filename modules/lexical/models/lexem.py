from modules.lexical.constants import LexemTypes


class Lexem:
    type: LexemTypes
    lex: int
    value: str

    def __init__(self, ltype: LexemTypes, lex, value) -> None:
        self.type = ltype
        self.lex = lex
        self.value = value

    def to_string(self):
        return f"lexem type: {self.type};\t lexem id: {self.lex};\t lexem value: {self.value}"
    
    def __repr__(self) -> str:
        return f"<Lexem {self.type} - {self.lex}>"