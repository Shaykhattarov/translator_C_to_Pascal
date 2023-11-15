from models import Token
from constants import Scopes



class SyntacticalProcessor:
    __lexems: list

    def __init__(self, lexems: list[object]) -> None:
        self.__lexems = lexems
        self.run()

    def run(self):
        pass


class SyntaxTree:

    def __init__(self, cargo, left = None, right = None) -> None:
        self.cargo = cargo
        self.left = left
        self.right = right

def print_tree(ast: SyntaxTree):
    if ast is None: return
    print(ast.cargo)
    print_tree(ast.left)
    print_tree(ast.right)


class SyntacticalTable:

    def __init__(self) -> None:
        self.head = None

    def add_to_end(self, token: Token, scope: Scopes):
        newnode = SyntacticalTableNode(token, scope)
        if self.head is None:
            self.head = newnode
            return 
        lastnode = self.head
        while lastnode.nextnode:
            lastnode = lastnode.nextnode
        lastnode.nextnode = newnode

    def contains(self, token: Token, scope: Scopes):
        lastnode = self.head
        while lastnode:
            if token == lastnode.token and scope == lastnode.scope:
                return True
            else:
                lastnode = lastnode.nextnode
        return False

    def index(self, nodeindex: int):
        lastnode = self.head
        nodenum: int = 0
        while nodenum <= nodeindex:
            if nodenum == nodeindex:
                return lastnode
            nodenum += 1
            lastnode = lastnode.nextnode
        return None

class SyntacticalTableNode:
    token: Token
    scope: str
    
    def __init__(self, token: Token = None, scope: int = None) -> None:
        self.token = token
        self.scope = scope
        self.nextnode = None