from processors import LexicalProcessor
import config


class Main:

    def __init__(self) -> None:
        self.__lexical_processor()

    def __lexical_processor(self):
        processor = LexicalProcessor()
        result = processor.process_file(file = config.INPUT_FILE)
        print(result)


if __name__ == "__main__":
    Main()