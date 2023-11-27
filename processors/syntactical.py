from models import Token, Float, Integer, Word
from typing import Union

class SyntaxTree:

    def __init__(self, cargo, left = None, right = None) -> None:
        self.cargo = cargo
        self.left = left
        self.right = right


class SyntacticalProcessor:
    __lexems: list

    def __init__(self, lexems: list[Union[Word, Integer, Float, Token]]) -> None:
        self.__lexems = lexems
        self.run()

    def run(self):
        pass

    def match():
        pass

    def print_syntax_tree(self, ast: SyntaxTree, level: int = 0):
        if ast != None:
            self.print_syntax_tree(ast.left, level + 1)
            print(' ' * 12 * level + '-> ' + str(ast.cargo))
            self.print_syntax_tree(ast.right, level + 1)
        else:
            print("Дерево не заполнено!")





