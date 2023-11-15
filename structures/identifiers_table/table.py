from models import *
from structures.syntax_tree import IdentifierNode


class IdentifiersTable:

    __table: dict[Token, IdentifierNode]

    def __init__(self, prev = None) -> None:
        self.__table: dict = {}
        self.__previous = prev

    def put(self, token: Token, identifier: IdentifierNode):
        self.__table[token] = identifier

    def get(self, token: Token):
        pass

    