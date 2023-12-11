from processors import LexicalProcessor, SyntacticalProcessor, SemanticProcessor, PascalGenerator
import config


class Main:

    def __init__(self) -> None:
        self.run()

    def run(self):
        lexems = self.__lexical_processor()
        ast = self.__syntactical_processor(lexems)
        analyz = self.__semantic_processor(lexems)
        pascal_code = self.__code_generator(ast)

    def __lexical_processor(self) -> list:
        processor = LexicalProcessor()
        lexems = processor.process_file(file = config.INPUT_FILE)
        self.__print_lexems(lexems)
        return lexems
        
    def __syntactical_processor(self, lex: list[object]):
        processor = SyntacticalProcessor(lexems = lex)
        self.__print_ast(processor.root)
        return processor.root
    
    def __semantic_processor(self, tokens: list):
        processor: SemanticProcessor = SemanticProcessor(tokens)
        return True

    def __code_generator(self, ast):
        processor: PascalGenerator = PascalGenerator(tree = ast, output = config.OUTPUT_FILE)
        processor.print_generated_code()
        return 

    def __print_lexems(self, lexems: list):
        print("-----------------------------------------------------")
        print("Parsed tokens")
        print("-----------------------------------------------------")
        for num, lex in enumerate(lexems):
            print(f"{num}. ", lex)

    def __print_ast(self, ast):
        ast.print_node()
        ast.print_node(0)


if __name__ == "__main__":
    Main()