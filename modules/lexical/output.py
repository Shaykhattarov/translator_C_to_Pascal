from modules.lexical.processor import LexicalProcessor


class LexicalAnalyzer:
    file: str
    result: object

    def __init__(self, file) -> None:
        self.file = file
        self.run()

    def run(self):
        processor: LexicalProcessor = LexicalProcessor()
        self.result = processor.process_file(filename = self.file)
        
        self.print_lexems()
        self.print_variables()

    def print_lexems(self):
        print("Lexems: ")
        print("================================================")
        for lexem in self.result[0]:
            print(lexem.to_string())
        print("================================================")

    def print_variables(self):
        print("Variables: ")
        print("================================================")
        for var in self.result[1]:
            print(var.to_string())
        print("================================================")
        
    def __repr__(self) -> str:
        return "<LexicalAnalyzer>"