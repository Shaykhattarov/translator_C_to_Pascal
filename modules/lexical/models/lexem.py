from modules.lexical.constants import LexemTypes


class Lexem:
    type: LexemTypes
    lex: int
    value: str
    description: str

    def __init__(self, ltype: LexemTypes, lex, value, description: str = None) -> None:
        self.type = ltype
        self.lex = lex
        self.value = value
        self.description = description
        

    def to_string(self):
        if self.description is not None:
            return f"Lexem type: <{self.type}> \t Lexem constants id: <{self.lex}> \t Lexem value: <{self.value}> \t Lexem description: {self.description}"
        else:
            return  f"Lexem type: <{self.type}> \t Lexem constants id: <{self.lex}> \t Lexem value: <{self.value}>"
    
    def __repr__(self) -> str:
        return f"<Lexem {self.type} - {self.lex}>"