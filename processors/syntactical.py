from models.token import Token
from constants import Tag

class SyntaxNode:

    def __init__(self, cargo) -> None:
        self.cargo = cargo
        self.left = self.right = None


class SyntaxTree:

    def __init__(self) -> None:
        self.root = None

    def __find(self, node: SyntaxNode, parent, value):
        if node is None:
            return None, parent, False
 
        if value == node.cargo:
            return node, parent, True
 
        if value < node.cargo:
            if node.left:
                return self.__find(node.left, node, value)
 
        if value > node.cargo:
            if node.right:
                return self.__find(node.right, node, value)
 
        return node, parent, False

    def append(self, obj: SyntaxNode):
        if self.root is None:
            self.root = obj
            return obj
 
        s, p, fl_find = self.__find(self.root, None, obj.cargo)
 
        if not fl_find and s:
            if obj.cargo < s.cargo:
                s.left = obj
            else:
                s.right = obj
 
        return obj
    
    def append_left(self, obj: SyntaxNode):
        if self.root is None:
            self.root = obj
            return obj
        s, p, fl_find = self.__find(self.root, None, obj.cargo)

        s.left = obj
        return obj
    
    def append_right(self, obj: SyntaxNode):
        if self.root is None:
            self.root = obj
            return obj
        
        s, p, fl_find = self.__find(self.root, None, obj.cargo)

        s.right = obj
        return obj
    
    def show_tree(self, node: SyntaxNode):
        if node is None:
            return
 
        self.show_tree(node.right)
        print(node.cargo)
        self.show_tree(node.left)
 
    def show_wide_tree(self, snode: SyntaxNode):
        if snode is None:
            return
 
        v = [snode]
        while v:
            vn = []
            for node in v:
                print(node.cargo, end="  ")
                if node.left:
                    vn += [node.left]
                if node.right:
                    vn += [node.right]
            print()
            v = vn



class SyntacticalProcessor:
    __lexems: list[Token]
    __current_token: Token
    __tree: SyntaxTree = SyntaxTree()
    __pointer: int = 0

    def __init__(self, lexems: list[Token]) -> None:
        self.__lexems = lexems
        self.parse_code()

    def parse_code(self):
        self.__tree.root = SyntaxNode(cargo = "Root") # Корневой элемент AST
        while self.__pointer < len(self.__lexems):
            if self.match(self.__pointer, [Tag.INT, Tag.FLOAT]):
                if self.match(self.__pointer + 2, [Tag.OP_PARENTHESES]) and self.match(self.__pointer + 1, [Tag.IDENTIFIER]):
                    raise Exception('"Функции" в данной версии синтаксического анализатора не поддерживаются!')

                if self.match(self.__pointer + 1, [Tag.IDENTIFIER]) and self.match(self.__pointer + 2, [Tag.ASSIGN]) and self.match(self.__pointer + 3, [self.__lexems[self.__pointer].tag]) and self.match(self.__pointer + 4, [Tag.EOS]):
                    self.__tree.root.left = SyntaxNode(cargo = f"{self.__lexems[self.__pointer + 2].tag}: {self.__lexems[self.__pointer + 2].lexeme}")
                    self.__tree.append(SyntaxNode(cargo = f"{self.__lexems[self.__pointer + 1].tag}: {self.__lexems[self.__pointer + 1].lexeme}"))
                    self.__tree.append(SyntaxNode(cargo = f"{self.__lexems[self.__pointer + 3].tag}: {self.__lexems[self.__pointer + 3].lexeme}"))
                    print(self.__tree.show_wide_tree(self.__tree.root))
                    

    def match(self, token_index: int, expected_tags: list[str]):
        if self.__lexems[token_index].tag in expected_tags:
            return True
        else:
            return False

    def stop(self):
        print("End")
        exit(0)
    



