from modules.lexical.output import LexicalAnalyzer
from modules.syntactical.output import SyntacticalAnalyzer


class Translator:
    inputfilepath: str = "E:/Study/Системы программного обеспечения/Лабораторная работа №1/Программа/data/input/main.cpp"
    outputfilepath: str = "E:/Study/Системы программного обеспечения/Лабораторная работа №1/Программа/data/output/main.pas"

    def __init__(self):
        self.lexical_processor()
        self.syntactical_processor()

    def lexical_processor(self):
        """ Запускает лексический анализатор и отдает токены """
        lexical = LexicalAnalyzer(self.inputfilepath)

    def syntactical_processor(self):
        syntactical = SyntacticalAnalyzer()
        
    
    


if __name__ == "__main__":
    Translator()