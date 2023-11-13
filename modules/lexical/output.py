from modules.lexical.processor import LexicalProcessor
import config
import os, json



class LexicalAnalyzer:
    file: str
    result: object

    def __init__(self, file) -> None:
        self.file = file
        self.run()

    def run(self):
        processor: LexicalProcessor = LexicalProcessor()
        self.result = processor.process_file(filename = self.file)

        print("Вывести в консоль список полученных лексем и переменных? Y|N")
        choose: str = input().upper()
        if choose == "Y" or choose == "YES":
            self.output()
            self.save()
        elif choose == "N" or choose == "NO":
            self.save()
        else:
            print("[ERROR] Ошибка ввода при выборе отображения в коносль.")
            exit(0)

    def save(self):
        if self.result is not None:
            if len(self.result[0]) != 0 and self.result[0] is not None:
                with open(os.path.join(config.SAVE_INTERMEDIATE_DATA_DIR, "lexem.json"), 'w', encoding='utf-8') as file:
                    json.dump([el.to_string() for el in self.result[0]], file)
            else:
                print("Список лексем пуст")
                exit(0)

            if len(self.result[1]) and self.result[1] is not None:
                with open(os.path.join(config.SAVE_INTERMEDIATE_DATA_DIR, "variables.json"), 'w', encoding='utf-8') as file:
                    json.dump([el.to_string() for el in self.result[1]], file)
            else:
                print("Список переменных пуст")
                exit(0)
        else:
            print("Списки лексем и переменных пусты")
            exit(0)

    def output(self):
        self.print_lexems()
        self.print_variables()

    def print_lexems(self):
        print("Lexems: ")
        print("================================================")
        for num, lexem in enumerate(self.result[0]):
            print(f"{num + 1}. ", lexem.to_string())
        print("================================================")

    def print_variables(self):
        print("Variables: ")
        print("================================================")
        for var in self.result[1]:
            print(var.to_string())
        print("================================================")
        
    def __repr__(self) -> str:
        return "<LexicalAnalyzer>"