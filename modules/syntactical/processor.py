from modules.lexical.models.lexem import Lexem



class SyntacticalProcessor:
    __lexem_list: list[Lexem]
    __pointer: int = 0
    __lexem: Lexem


    def __init__(self, lexems) -> None:
        self.__lexems = lexems

    def process_lexems(self):
        while self.__pointer != len(self.__lexem_list):
            self.__get_next_lexem()
            
            match self.__lexem:
                case "asdasd":
                    continue

    def __get_next_lexem(self):
        self.__lexem = self.__lexem_list[self.__pointer] 
        self.__pointer += 1