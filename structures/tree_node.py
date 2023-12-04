from models import Token
from structures import TreeNodeType


class TreeNode:

    def __init__(self, token: Token, nodetype: TreeNodeType, scope: SymbolTable) -> None:
        self.parent = None
        self.token = token