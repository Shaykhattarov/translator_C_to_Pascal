from models import Token, Symbol, SymbolType
from constants import Tag
from structures import TreeNode, TreeNodeType, SymbolTable
from structures.tree_node_type import TREE_NODE_TYPE_MNEMONIC


class PascalGenerator:
    __tree: TreeNode
    __lines: list[str] = []
    __output: str
    code: str = ""

    def __init__(self, tree: TreeNode, output: str) -> None:
        self.__tree = tree
        self.__output = output
        self.generator()
        #print('\n[INFO]', "Строки: ", self.__lines, end='\n\n')

    def prepare_generator(self):
        self.__lines.append("program main;\n")

    def generator(self):
        self.prepare_generator() # Подготовка файла к сохранению
        self.start_generator() # Генерация кода
        self.save_generated_code() # Сохранение сгенерированного файла

    def save_generated_code(self):
        for num, line in enumerate(self.__lines):
            if num == len(self.__lines) - 1:
                line = line.replace(';', '.')

            self.code += line
            if '\t' not in line:
                self.code += '\n'

        with open(self.__output, 'w', encoding='utf-8') as file:
            file.write(self.code)
        
        return self.code
        
    def print_generated_code(self):
        print("-----------------------------------------------------")
        print("Generated Pascal code")
        print("-----------------------------------------------------")
        print(self.code)
        
    def start_generator(self):
        node: TreeNode = self.__tree
        if TREE_NODE_TYPE_MNEMONIC[self.__tree.nodetype] == "EMPTY":
            if len(self.__tree.childs) != 1:
                raise Exception("Ошибка генерации! Пришло неожидаемое количество потомков AST!")
            node = self.__tree.childs[0]

        if TREE_NODE_TYPE_MNEMONIC[node.nodetype] == "MODULE":
            self.generate_module() # Добавляем блок 'begin' в программу
            for child in node.childs:
                # Тут можно изменить функциональность, чтобы просматривать большой одной функции main
                if child.token.lexeme == "main":
                    node = child
                    break
            
        if TREE_NODE_TYPE_MNEMONIC[node.nodetype] == "FUNCTION":
            for child in node.childs:
                # Тут можно изменить функциональность для считывания аргументов и типа данных функции
                if child.token.lexeme == "BLOCK":
                    self.generate_block(child)
                    break
        
    def generate_module(self):
        self.__lines.append("begin")
        return 

    def generate_block(self, node: TreeNode, depth: int = 1):
        for child in node.childs:
            if TREE_NODE_TYPE_MNEMONIC[child.nodetype] == "TYPE" and child.childs[0].token.tag == Tag.IDENTIFIER:
                self.__lines.append('\t' * depth)
                self.generate_declaration(child)
                continue

            if TREE_NODE_TYPE_MNEMONIC[child.nodetype] == "ASSIGNMENT":
                self.__lines.append('\t' * depth)
                self.generate_assignment(child)
                continue

            if TREE_NODE_TYPE_MNEMONIC[child.nodetype] == "WHILE":
                self.__lines.append('\t' * depth)
                self.generate_while(child)
                continue

            if TREE_NODE_TYPE_MNEMONIC[child.nodetype] == "SYMBOL":
                self.__lines.append('\t' * depth)
                self.generate_assignment(child)
                continue

        self.__lines.append('end;')

    def generate_declaration(self, node: TreeNode):
        if len(node.childs) == 1 and node.childs[0].token.tag == Tag.IDENTIFIER:
            variable_name: str = node.childs[0].token.lexeme
            variable_type: str = node.token.lexeme
            self.__lines.append(f"var {variable_name}: {variable_type};")
            return 

    def generate_assignment(self, node: TreeNode):
        buffer = ""
        for child in node.childs:
            if TREE_NODE_TYPE_MNEMONIC[child.nodetype] == "SYMBOL":
                buffer += f"{child.token.lexeme} := "
            
            if TREE_NODE_TYPE_MNEMONIC[child.nodetype] == "CONSTANT":
                buffer += child.token.lexeme

            if TREE_NODE_TYPE_MNEMONIC[child.nodetype] == "BINARY_OP":
                buffer += self.generate_operation(child)

        buffer += ";"
        self.__lines.append(buffer)
        return 
        
    def generate_operation(self, node: TreeNode):
        terms: list = [] 
        for child in node.childs:
            if TREE_NODE_TYPE_MNEMONIC[child.nodetype] == "SYMBOL" or TREE_NODE_TYPE_MNEMONIC[child.nodetype] == "CONSTANT":
                terms.append(child.token.lexeme)
            else:
                raise Exception("Более сложные конструкции выражений не реализованы в этой версии транслятора!")
        
        if terms[0] == '0' and node.token.lexeme == '-': 
            return '-' + terms[1]
        
        return f" {node.token.lexeme} ".join(terms)

    def generate_while(self, node: TreeNode):
        buffer: str = "while " 
        for child in node.childs:
            if TREE_NODE_TYPE_MNEMONIC[child.nodetype] == "SYMBOL":
                buffer += child.token.lexeme + " do"
                self.__lines.append(buffer)
            
            if TREE_NODE_TYPE_MNEMONIC[child.nodetype] == "CONSTANT" and (child.token.lexeme == '1' or child.token.lexeme == '0'):
                if child.token.lexeme == '1':
                    buffer += "True do"
                elif child.token.lexeme == '0':
                    buffer += "False do"
                else:
                    raise Exception("В условие может попасть константа, но это может быть только '1' или '0'!")
                self.__lines.append(buffer)

            if TREE_NODE_TYPE_MNEMONIC[child.nodetype] == "BINARY_OP":
                state = self.generate_statement(child)
                buffer += state
                buffer += " do"
                self.__lines.append(buffer)

            if TREE_NODE_TYPE_MNEMONIC[child.nodetype] == "BLOCK":
                self.generate_block(child, depth=2) 

    def generate_statement(self, node: TreeNode):
        buffer: str = ''
        terms: list = []
        
        for child in node.childs:
            if TREE_NODE_TYPE_MNEMONIC[child.nodetype] == "SYMBOL" or TREE_NODE_TYPE_MNEMONIC[child.nodetype] == "CONSTANT":
                terms.append(child.token.lexeme)
            
            if TREE_NODE_TYPE_MNEMONIC[child.nodetype] == "BINARY_OP":
                oper = self.generate_operation(child)
                terms.append(oper)

        return f' {node.token.lexeme} '.join(terms) 
            