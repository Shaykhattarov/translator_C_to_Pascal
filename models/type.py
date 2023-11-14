from models.word import Word

class Type(Word):
    width: int = 0

    def __init__(self, s: str, tag: int, width: int):
        super().__init__(s, tag)
        self.width = width