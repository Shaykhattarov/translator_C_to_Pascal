from models import Token
from constants.tag import Tag
from models.ast import StatementsNode, ExpressionNode

class SyntaxTree:

    def __init__(self, cargo, left = None, right = None) -> None:
        self.cargo = cargo
        self.left = left
        self.right = right


class SyntacticalProcessor:
    __lexems: list[Token]
    __pointer: int = 0
    __scope: dict = {}

    def __init__(self, lexems: list[Token]) -> None:
        self.__lexems = lexems
        self.run()

    def parse_code(self) -> ExpressionNode:
        root = StatementsNode()
        while self.__pointer < len(self.__lexems):
            code_string_node = self.parse_expression()
            self.require(expected_tags=[Tag.EOS])
            root.add_node(code_string_node)
        return root


    def match(self, expected_tags: list) -> Token | None:
        if self.__pointer < len(self.__lexems):
            current_token: Token = self.__lexems[self.__pointer]
        if current_token.tag in expected_tags:
            self.__pointer += 1
            return current_token
        return None

    def require(self, expected_tags: list) -> Token:
        token = self.match(expected_tags)
        if token is None:
            raise Exception(f"[ERROR] Позиция: {self.__pointer}. Ожидаемый тип токена не совпал с текущим!")
        return token

    def print_syntax_tree(self, ast: SyntaxTree, level: int = 0):
        if ast != None:
            self.print_syntax_tree(ast.left, level + 1)
            print(' ' * 12 * level + '-> ' + str(ast.cargo))
            self.print_syntax_tree(ast.right, level + 1)
        else:
            print("Дерево не заполнено!")





