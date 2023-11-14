from modules.syntactical.processor import SyntacticalProcessor
from modules.lexical.models.lexem import Lexem

class SyntacticalAnalyzer:
    __lexems: list[Lexem]
    result: str

    def __init__(self, lexems: list[Lexem]) -> None:
        self.__lexems = lexems
        self.run()

    def run(self):
        processor: SyntacticalProcessor = SyntacticalProcessor(lexems = self.__lexems)
        processor.process_lexems()