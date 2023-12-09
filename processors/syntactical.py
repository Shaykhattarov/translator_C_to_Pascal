from models.token import Token
from models import SymbolType
from constants import Tag
from structures import SymbolTable, TreeNode
from structures.tree_node_type import TreeNodeType


class SyntacticalProcessor:
    __lexems: list[Token]
    root: TreeNode
    __root_symbol_table: SymbolTable = SymbolTable(name="GLOBAL")
    __token_pointer: int = 0
    __block_counter: int = 0 


    def __init__(self, lexems) -> None:
        self.__lexems = lexems
        self.build_syntax_tree()
        
    def get_symbol_table(self):
        return self.__root_symbol_table
    
    def get_syntax_tree(self):
        return self.root

    def build_syntax_tree(self):
        # add iput system function to symbols table (write int to std out)
        iput: Token = Token(lex="iput", tag=Tag.IDENTIFIER)
        self.__root_symbol_table.add_symbol(iput, SymbolType.FUNCTION)
        symbol = self.__root_symbol_table.look_up_symbol(iput)
        if symbol: 
            symbol.arg_count = 1

        # add iget system function to symbols table (write int to std in)
        iget: Token = Token(lex="iget", tag=Tag.IDENTIFIER)
        self.__root_symbol_table.add_symbol(iget, SymbolType.FUNCTION)
        symbol = self.__root_symbol_table.look_up_symbol(iget)
        if symbol: 
            symbol.arg_count = 1

        self.root: TreeNode = self.parse_module(self.__root_symbol_table)
        self.root.print_node()
        self.root.print_node(0)
        



    #---------------------------------------------------------------------------
    # <module> ::= { <declaration> | <function> }*
    #---------------------------------------------------------------------------
    def parse_module(self, scope):
        program: TreeNode = TreeNode(Token(lex="", tag=Tag.EMPTY), TreeNodeType.MODULE, scope)
        function_check: Token
        function_check = self.get_token(self.__token_pointer + 2)
        if function_check.tag == Tag.OP_PARENTHESES:
            program.add_child(self.parse_function(scope))
        else:
            raise Exception("Ожидалось объявление функции!")
        
        #while(self.next()):
        #    function_check = self.get_token(self.__token_pointer + 2)
        #    if function_check.tag == Tag.OP_PARENTHESES:
        #        program.add_child(self.parse_function(scope))
        #    else:
        #        raise Exception("Ожидалось объявление функции!")
        return program
    

    #---------------------------------------------------------------------------
    # <function> ::= <type> <identifier> '(' <argument> {, <argument>}* ')' <block>
    #---------------------------------------------------------------------------
    def parse_function(self, scope: SymbolTable):
        data_type: Token = self.get_token()
        if not self.is_data_type(data_type.tag): raise Exception("Ожидался токен типа данных!")
        return_type: TreeNode = TreeNode(data_type, TreeNodeType.TYPE, scope)
        self.next()
        self.check_token(tokentag=Tag.IDENTIFIER)
        func: TreeNode = TreeNode(self.get_token(), TreeNodeType.FUNCTION, scope)
        if not scope.add_symbol(func.get_token, SymbolType.FUNCTION): 
            raise Exception("Функция уже объявлена!")
        else: 
            self.next()

        funcname: str = f"{func.get_token.lexeme} - {func.get_token.length}"
        block_symbol: SymbolTable = SymbolTable(name = funcname)
        scope.add_child(block_symbol)
        arguments: TreeNode = TreeNode(Token("Arguments", Tag.EMPTY), TreeNodeType.SYMBOL, block_symbol)
        while(self.next()):
            tkn: Token = self.get_token()
            if self.is_token_type(Tag.COMMA): 
                self.next()
            elif self.is_token_type(Tag.CL_PARENTHESES):
                break
            elif not tkn.lexeme.isalpha() and not tkn.lexeme.isdigit():
                raise Exception("Неожидаемый тип токена в аргументах функции!")
            arguments.add_child(self.parse_arguments(block_symbol))
        self.next()

        # save function params count
        f = scope.look_up_symbol(func.get_token)
        f.arg_count = arguments.get_child_count
        function_body = self.parse_block(block_symbol, True, False)

        func.add_child(return_type)
        func.add_child(arguments)
        func.add_child(function_body)

        return func
    

    #---------------------------------------------------------------------------
    # <argument> :: = <type> <identifier>
    #---------------------------------------------------------------------------
    def parse_arguments(self, scope: SymbolTable):
        data_type: Token = self.get_token()
        if not self.is_data_type(data_type.tag):
            raise Exception("Ожидался агрумент функции")
        
        argument: TreeNode = TreeNode(data_type, TreeNodeType.TYPE, scope)
        self.next()
        self.check_token(Tag.IDENTIFIER)
        variable_name: TreeNode = TreeNode(self.get_token(), TreeNodeType.SYMBOL, scope)
        if not scope.add_symbol(variable_name.get_token, SymbolType.ARGUMENT):
            raise Exception("Аргумент уже объявлен!")
        argument.add_child(variable_name)
        return argument
    

    #---------------------------------------------------------------------------
    # <block> ::= '{' {<statement>}* '}'
    #---------------------------------------------------------------------------
    def parse_block(self, scope: SymbolTable, is_function: bool, while_block: bool):
        block: TreeNode = TreeNode(Token("BLOCK", Tag.NONE), TreeNodeType.BLOCK, scope)
        block_symbols: SymbolTable
        if is_function:
            block_symbols = scope
        else:
            name: str = "block"
            self.__block_counter += 1
            name += f" {self.__block_counter}"
            block_symbols = SymbolTable(name)
            scope.add_child(block_symbols)
            block.set_symbol_table(block_symbols)
        
        while(self.next()):
            if self.is_token_type(Tag.CL_BRACES): 
                break
            if self.is_token_type(Tag.EOS):
                continue
            block.add_child(self.parse_statement(block_symbols, while_block))
        
        return block
    

    #---------------------------------------------------------------------------
    # <statement> ::= <block> | <declration> | <assign> | <if-else> | <while> | <jump> | <call>
    #---------------------------------------------------------------------------
    def parse_statement(self, scope: SymbolTable, while_block: bool):
        token: Token = self.get_token()
        if self.is_data_type(token.tag):
            return self.parse_declaration(scope)
        elif token.tag == Tag.OP_BRACES:
            return self.parse_block(scope, False, while_block)
        elif token.tag == Tag.IDENTIFIER:
            next_token: Token = self.get_next_token()
            if next_token.tag == Tag.ASSIGN:
                return self.parse_assignment(scope)
            # Не рабочая фича
            #if next_token.tag == Tag.OP_PARENTHESES:
            #    call_node: TreeNode = self.parse_call(scope)
            #    self.next()
            #    if not self.is_token_type(Tag.EOS):
            #        raise Exception("';' ожидалось")
            #    return call_node
            elif next_token in [Tag.INCREMENT, Tag.DECREMENT]:
                return self.parse_expression(scope)
            else:
                raise Exception("Неожидаемый токен, ожидались равно '=' или вызов функции!")
        elif token.tag == Tag.IF: return self.parse_if_else(scope, while_block)
        elif token.tag == Tag.WHILE: return self.parse_while(scope)
        elif token.tag == Tag.BREAK: raise Exception("Тип токена 'break' не обрабатывается в этой версии!")
        else: raise Exception("Неожидаемый токен!")


    #---------------------------------------------------------------------------
    # <while> :: = 'while' '(' < expression > ')' < statement >
    #---------------------------------------------------------------------------
    def parse_while(self, scope: SymbolTable):
        while_block: TreeNode = TreeNode(self.get_token(), TreeNodeType.WHILE, scope)
        self.next()
        self.check_token(Tag.OP_PARENTHESES)
        self.next()
        while_block.add_child(self.parse_logical(scope))
        self.next()
        self.check_token(Tag.CL_PARENTHESES)
        self.next()
        while_block.add_child(self.parse_statement(scope, True))
        return while_block
    

    #---------------------------------------------------------------------------
    # <if-else> ::= 'if' '(' <expression> ')' <statement> { 'else' <statement> }
    #---------------------------------------------------------------------------
    def parse_if_else(self, scope: SymbolTable, while_block: bool):
        if_block: TreeNode = TreeNode(self.get_token(), TreeNodeType.IF_ELSE, scope)
        self.next()
        self.check_token(Tag.OP_PARENTHESES)
        self.next()
        if_block.add_child(self.parse_logical(scope))
        self.check_token(Tag.CL_PARENTHESES)
        self.next()
        if_block.add_child(self.parse_statement(scope, while_block))
        if self.get_next_token().tag == Tag.ELSE:
            self.next()
            self.next()
            if_block.add_child(self.parse_statement(scope, while_block))
        return if_block

    #---------------------------------------------------------------------------
    # <declaration> ::= <type> <identifier> {','<identifier>}* ';'
    #---------------------------------------------------------------------------
    def parse_declaration(self, scope: SymbolTable):
        data_type = self.get_token()
        if not self.is_data_type(data_type.tag): raise Exception("Ожидался тип данных!")
        variable_declaration: TreeNode = TreeNode(data_type, TreeNodeType.TYPE, scope)
        while(self.next()):
            if self.is_token_type(Tag.COMMA): self.next()
            elif self.is_token_type(Tag.EOS): break
            self.check_token(Tag.IDENTIFIER)
            variable_name: TreeNode = TreeNode(self.get_token(), TreeNodeType.SYMBOL, scope)
            if not scope.add_symbol(variable_name.get_token, SymbolType.VARIABLE):
                raise Exception("Переменная уже инициализирована!")
            variable_declaration.add_child(variable_name)
        return variable_declaration
    

    #---------------------------------------------------------------------------
    # <assign> ::= <identifier> = <expression> ';'
    #---------------------------------------------------------------------------
    def parse_assignment(self, scope: SymbolTable):
        identifier: Token = self.get_token()
        if scope.look_up_symbol(identifier) is None:
            raise Exception("Символ не известен")
        self.next()
        self.check_token(Tag.ASSIGN)
        op: TreeNode = TreeNode(self.get_token(), TreeNodeType.ASSIGNMENT, scope)
        self.next()
        a: TreeNode = TreeNode(identifier, TreeNodeType.SYMBOL, scope)
        b: TreeNode = self.parse_logical(scope)
        op.add_child(a)
        op.add_child(b)
        return op
    

    #---------------------------------------------------------------------------
    # *  <logical>     ::= <comparison> {( && | '||') <comparison>}
    #---------------------------------------------------------------------------
    def parse_logical(self, scope: SymbolTable):
        prev_op = op = None
        operand1 = self.parse_comparison(scope)
        token: Token = self.get_token()
        while self.is_logical(token.tag):
            self.next()
            operand2 = self.parse_comparison(scope)
            op = TreeNode(token, TreeNodeType.BINARY_OP, scope)
            if prev_op is None:
                op.add_child(operand1)
            else:
                op.add_child(prev_op)
            op.add_child(operand2)
            prev_op = op
            token = self.get_token()
            self.next()
        if op is None:
            return operand1
        else:
            return op
        

    #---------------------------------------------------------------------------
    # <comparison>  :: = <expression>{ (== | != | > | >= | < | <=) < expression > }
    #---------------------------------------------------------------------------
    def parse_comparison(self, scope: SymbolTable):
        operand1 = self.parse_expression(scope)
        operand2 = None
        op = None
        prev_op = None
        token = self.get_token()
        while self.is_comparison(token.tag):
            self.next()
            operand2 = self.parse_expression(scope)
            op = TreeNode(token, TreeNodeType.BINARY_OP, scope)
            if prev_op is None: 
                op.add_child(operand1)
            else:
                op.add_child(prev_op)
            op.add_child(operand2)
            prev_op = op
            token = self.get_token()
        if op is None:
            return operand1
        else:
            return op
        

    #---------------------------------------------------------------------------
    # <expression> ::= <term> {(+|-) <term>}
    #---------------------------------------------------------------------------
    def parse_expression(self, scope: SymbolTable):
        operand1 = self.parse_term(scope)
        operand2 = None
        op = None
        prev_op = None
        token = self.get_token()
        while self.is_token_type(Tag.PLUS) or self.is_token_type(Tag.MINUS):
            self.next()
            operand2 = self.parse_term(scope)
            op = TreeNode(token, TreeNodeType.BINARY_OP, scope)
            if prev_op is None:
                op.add_child(operand1)
            else:
                op.add_child(prev_op)
            op.add_child(operand2)
            prev_op = op
            token = self.get_token()
        if op is None:
            return operand1
        else:
            return op
        

    #---------------------------------------------------------------------------
    # <term>  ::= <bitwise> {(*|/) <bitwise>}
    #---------------------------------------------------------------------------
    def parse_term(self, scope):
        operand1 = self.parse_bitwise(scope)
        operand2 = None
        op = None
        prev_op = None
        token = self.get_token()
        while self.is_token_type(Tag.MULTI) or self.is_token_type(Tag.DIVIDE):
            self.next()
            operand2 = self.parse_bitwise(scope)
            op = TreeNode(token, TreeNodeType.BINARY_OP, scope)
            if prev_op is None:
                op.add_child(operand1)
            else:
                op.add_child(prev_op)
            op.add_child(operand2)
            prev_op = op
            token = self.get_token()
        if op is None:
            return operand1
        else:
            return op
        

    #---------------------------------------------------------------------------
    # <bitwise>  ::= <factor> {( & | '|' | ^ | << | >> ) <factor>}
    #---------------------------------------------------------------------------
    def parse_bitwise(self, scope):
        operand1 = self.parse_factor(scope)
        operand2 = None
        op = None
        prev_op = None
        token = self.get_token()
        while self.is_bitwise(token.tag):
            self.next()
            operand2 = self.parse_factor(scope)
            op = TreeNode(token, TreeNodeType.BINARY_OP, scope)
            if prev_op is None:
                op.add_child(operand1)
            else:
                op.add_child(prev_op)
            op.add_child(operand2)
            prev_op = op
            token = self.get_token()
        if op is None:
            return operand1
        else:
            return op
    
    #---------------------------------------------------------------------------
    # <factor> ::= ({~|!|-|+} <number>) | <identifer> | <call>
    #---------------------------------------------------------------------------
    def parse_factor(self, scope: SymbolTable):
        factor = None
        unary_minus = bitwise_not = logical_not = False

        #print(self.get_token(), '[INFO]')
        if self.is_token_type(Tag.MINUS):
            unary_minus = True
            self.next()
        elif self.is_token_type(Tag.PLUS):
            unary_minus = False
            self.next()
        elif self.is_token_type(Tag.NONE):
            bitwise_not = True
            self.next()
        elif self.is_token_type(Tag.NOT_EQUAL):
            logical_not = True
            self.next()

        if self.is_token_type(Tag.OP_PARENTHESES):
            self.next()
            factor = self.parse_expression(scope)
            token: Token = self.get_token()
            if self.is_token_type(Tag.CL_PARENTHESES):
                self.next()
            else:
                raise Exception("Ожидалось закрытие фигурной кавычки")
        elif self.is_token_type(Tag.CONSTANT):
            factor = TreeNode(self.get_token(), TreeNodeType.CONSTANT, scope)
        elif self.is_token_type(Tag.IDENTIFIER):
            next_token: Token = self.get_next_token()
            if next_token.tag == Tag.OP_PARENTHESES:
                factor = self.parse_call(scope)
                self.next()
            else:
                factor = TreeNode(self.get_token(), TreeNodeType.SYMBOL, scope)
                if scope.look_up_symbol(self.get_token()) is None:
                    raise Exception("Символ неизвестен!")
                self.next()
        else:
            raise Exception("Ожидались число или идентификатор!")
        
        if unary_minus:
            expr: TreeNode = TreeNode(Token("-", Tag.MINUS), TreeNodeType.BINARY_OP, scope)
            zero: TreeNode = TreeNode(Token("0", Tag.CONSTANT), TreeNodeType.CONSTANT, scope)
            expr.add_child(zero)
            expr.add_child(factor)
            return expr

        
        return factor


    def get_token_count(self):
        return len(self.__lexems)
    
    def get_token(self, index=None):
        if index is None:
            return self.__lexems[self.__token_pointer]
        return self.__lexems[index]
    
    def get_next_token(self):
        return self.__lexems[self.__token_pointer + 1]

    def next(self):
        self.__token_pointer += 1
        return self.__token_pointer < self.get_token_count()
    
    def is_data_type(self, tokentag: Tag):
        return tokentag in [Tag.FLOAT, Tag.INT]
    
    def is_comparison(self, tokentag: Tag):
        return tokentag in [Tag.EQUAL, Tag.GR_EQUAL, Tag.LR_EQUAL, Tag.NOT_EQUAL, Tag.GREATER, Tag.LOWER]
    
    def is_logical(self, tokentag: Tag):
        return tokentag in [Tag.AND, Tag.OR]
    
    def is_bitwise(self, tokentag: Tag):
        return tokentag == Tag.AND or tokentag == Tag.NONE or tokentag == Tag.OR

    def is_token_type(self, tokentag: Tag):
        return self.get_token().tag == tokentag 

    def check_token(self, tokentag: Tag):
        if not self.is_token_type(tokentag):
            raise Exception("Данного типа токена не существует!")    