from models import Token
from structures.tree_node_type import TreeNodeType, TREE_NODE_TYPE_MNEMONIC
from structures.symbol_table import SymbolTable



class TreeNode:
    childs: list = []
    nodetype: TreeNodeType
    scope: SymbolTable
    token: Token
    symbols: SymbolTable = None

    def __init__(self, token: Token, nodetype: TreeNodeType, scope: SymbolTable) -> None:
        self.parent = None
        self.token = token
        self.nodetype = nodetype
        self.scope = scope

    def __repr__(self) -> str:
        return f"<TreeNode {self.token} - {self.nodetype} - {self.scope}>"

    def __del__(self):
        self.remove_all()

    def add_child(self, node):
        if node is None: return None
        node.parent = self
        self.childs.append(node)
        return node

    def remove_all(self):
        child_count = len(self.childs)
        self.childs = []

    def remove_child(self, node) -> bool:
        for entry in self.childs:
            if entry == node:
                self.childs.remove(node)
                return True
        return False
    
    @property
    def get_type(self):
        return self.nodetype
    
    @property
    def get_token(self):
        return self.token

    def get_parent(self):
        return self.parent
    
    def get_child(self, index: int):
        if index >= len(self.childs): return None
        return self.childs[index]
    
    @property
    def get_child_count(self):
        return len(self.childs)
    
    def set_symbol_table(self, scope: SymbolTable):
        self.symbols = scope
    
    def get_depth(self) -> int:
        depth: int = 0
        node = self.get_parent()
        while node is not None:
            depth += 1
            node = node.get_parent()
        return depth
    
    def print_node(self, tab: int = None):
        if tab is None:
            print("-----------------------------------------------------")
            print("Parsed abstract syntax tree")
            print("-----------------------------------------------------")
        else:
            for i in range(tab):
                if i < (tab - 1):
                    print("| ", end="")
                else:
                    print("|-", end="")
            print("'", end="")
            print(f"{self.token.lexeme} - {self.token.length}", end="")
            print("'", "(", TREE_NODE_TYPE_MNEMONIC[int(self.nodetype)], ")", end="")
            print(" ", self.scope.name)
            for node in self.childs:
                node.print_node(tab + 1)
