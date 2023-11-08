from modules.lexical.output import LexicalAnalyzer


class Translator:
    inputfilepath: str = "E:/Study/Системы программного обеспечения/Лабораторная работа №1/Программа(1)/data/input/main.cpp"
    outputfilepath: str = "E:/Study/Системы программного обеспечения/Лабораторная работа №1/Программа(1)/data/output/main.pas"

    def __init__(self):
        result: list = self.lexical_processor()

    def lexical_processor(self) -> []:
        """ Запускает лексический анализатор и отдает токены """
        lexical = LexicalAnalyzer(self.inputfilepath)
        
    
    


if __name__ == "__main__":
    Translator()