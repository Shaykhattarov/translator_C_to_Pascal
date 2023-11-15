from processors import LexicalProcessor, SyntacticalProcessor
import config


class Main:

    def __init__(self) -> None:
        self.__lexical_processor()
        self.run()

    def run(self):
        lexems = self.__lexical_processor()
        for num, lex in enumerate(lexems):
            print(f"{num}. ", lex)
        ast = self.__syntactical_processor(lex = lexems)

    def __lexical_processor(self):
        processor = LexicalProcessor()
        return processor.process_file(file = config.INPUT_FILE)

    def __syntactical_processor(self, lex: list[object]):
        processor = SyntacticalProcessor(lexems = lex)


if __name__ == "__main__":
    Main()