from models import Token
from constants.tag import Tag
from models.ast import StatementsNode, ExpressionNode
from structures.linked_list import Table, TableNode


class SyntacticalProcessor:
    __lexems: list[Token]
    __token: Token
    __pointer: int = 0
    __head: Table = None

    def __init__(self, lexems: list[Token]) -> None:
        self.__lexems = lexems
        self.move()

    def move(self):
        if self.__pointer < len(self.__lexems):
            self.__token = self.__lexems[self.__pointer]
        else:
            raise Exception("Список токенов закончился")
        
    def error(self):
        raise Exception(f"Error on token №{self.__pointer} - {self.__token}")

    def program(self):
        statement_node: StatementsNode = self.block()
        print(statement_node.to_string())
        return statement_node

    def match(self, expected_tag: list):
        if self.__token.tag in expected_tag:
            self.move()
        else:
            raise Exception("Syntax error")

    def block(self):
        self.match(['{'])
        table: Table = self.__head
        self.__head: Table = Table()
        


    def declare(self):
        while self.__token.tag in [Tag.ARRAY, Tag.BOOLEAN, Tag.CHAR, Tag.INT, Tag.FLOAT]:
            pass
        
    