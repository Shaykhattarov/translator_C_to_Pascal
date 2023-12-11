from constants import Tag
from models import Token

class SemanticProcessor:
    __tokens: list[Token]
    __pointer: int = 0
    __token: Token
    __variables: list = []

    def __init__(self, tokens: list[Token]) -> None:
        self.__tokens = tokens
        self.semantic_processor()

    def semantic_processor(self):
        for index in range(len(self.__tokens)):
            if self.is_data_type(self.__tokens[index]):
                if self.is_identifier(self.__tokens[index + 1]):
                    identifier: Token = self.__tokens[index + 1]
                    self.check_identifier(identifier)
                    if identifier in self.__variables:
                        raise Exception("Повторное объявление идентификаторов!")
                    else:
                        self.__variables.append(identifier.lexeme)
            
            if self.is_identifier(self.__tokens[index]) and not self.is_data_type(self.__tokens[index - 1]):
                if self.__tokens[index].lexeme not in self.__variables:
                    print(index, self.__tokens[index], self.__variables)
                    raise Exception("Необъявленный идентификатор!")
        
        self.print_good()
        return
        
    def print_good(self):
        print("-----------------------------------------------------")
        print("Semantic analyz is verified")
        print("-----------------------------------------------------")

    def is_data_type(self, token: Token):
        return token.tag in [Tag.INT, Tag.FLOAT]

    def is_identifier(self, token: Tag):
        return token.tag == Tag.IDENTIFIER

    def check_identifier(self, identifier: Token):
        name = identifier.lexeme
        if name in ["ALL", "AND", "BY", "EQ", "GE", "GT", "LE", "LT", "NE", 'NOT', "OR", "TO", "WITH"]:
            raise Exception("В именах переменных не могут использоваться зарезервированные ключевые слова!")
        elif name[len(name) - 1] == "_":
            raise Exception("Следует избегать имен переменных, заканчивающихся символом подчеркивания, поскольку возможен конфликт с именами, создаваемыми автоматически командами и процедурами!")
        elif name[0] == "." or name[len(name) - 1] == ".":
            raise Exception("Имена переменных не должны начинаться или заканчиваться точкой!")
        elif name[0] == "#" or name[0] == "$":
            raise Exception("Символы '#' и '$' не разрешены в качестве первых символов пользовательской переменной!")
        elif " " in name:
            raise Exception("Имена переменных не могут содержать пробелов!")
        elif name[0] in [str(el) for el in range(9)]:
            raise Exception("Имя переменной не может начинаться с цифры!")
        else:
            return True