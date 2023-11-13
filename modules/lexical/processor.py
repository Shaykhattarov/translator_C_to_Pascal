from modules.lexical.constants import Constants, LexemTypes, LexemProcessorStates
from modules.lexical.models import Lexem, Variable


class LexicalProcessor:
    __filedata: str
    __error: str
    __buffer: str = ""
    __char: str = ''
    __state = LexemProcessorStates.Idle
    __pointer: int = 0
    __lexems: list[Lexem] = []
    __variables_table: list[Variable] = []
    __is_float = False

    def process_file(self, filename: str):
        self.__filedata = self.__read_file(file = filename)
        self.__char = self.__filedata[0]

        while self.__state != LexemProcessorStates.Final and self.__pointer < len(self.__filedata) - 1:
            match self.__state:
                case LexemProcessorStates.Final:
                    break

                case LexemProcessorStates.Error:
                    self.__state = LexemProcessorStates.Final
                    print(self.__error)

                case LexemProcessorStates.Idle:
                    if self.__is_empty_or_next_line(input = self.__char):
                        self.__get_next_char()
        
                    elif self.__char.isalpha():
                        self.__clear_buffer()
                        self.__add_to_buffer(input = self.__char)
                        self.__state = LexemProcessorStates.ReadingIdentifier
                        self.__get_next_char()
                    
                    elif self.__char.isdigit():
                        self.__clear_buffer()
                        self.__add_to_buffer(input = self.__char)
                        self.__state = LexemProcessorStates.ReadingNum
                        self.__get_next_char()

                    elif self.__char in Constants.Literal:
                        self.__clear_buffer()
                        self.__add_to_buffer(input = self.__char)
                        self.__state = LexemProcessorStates.ReadingLiteral
                        self.__get_next_char()
                    
                    else:
                        self.__clear_buffer()
                        self.__state = LexemProcessorStates.Delimeter
                        self.__add_to_buffer(input = self.__char)
                        self.__get_next_char()
                    
                    continue
                        
                
                case LexemProcessorStates.ReadingIdentifier:
                    if self.__char.isalpha() or self.__char.isdigit():
                        self.__add_to_buffer(input = self.__char)
                        self.__get_next_char()

                    else:
                        search_lexem = self.search_in_lexem_dictionary()
                        search_types = self.search_in_types_dictionary()

                        if search_lexem[0] != -1:
                            self.__add_lexem(ltype = LexemTypes.Identifier, lex = search_lexem[0], value = search_lexem[1], description = self.__buffer)
                            self.__clear_buffer()

                        elif search_types[0] != -1:
                            self.__add_lexem(ltype = LexemTypes.DataType, lex = search_types[0], value = search_types[1], description=self.__buffer)
                            self.__clear_buffer()

                        else:
                            is_variable = self.__buffer in [var.name for var in self.__variables_table]

                            if not is_variable:
                                variable_type = self.__lexems[-1]
                                if variable_type is None:
                                    self.__state = LexemProcessorStates.Error
                                    self.__error = f"[ERROR] Отсутствует тип переменной {self.__buffer}. Остановка произошла на символе №{self.__pointer}."
                                    continue

                                self.__variables_table.append(Variable(vid = len(self.__variables_table), data_type = variable_type.lex, name = self.__buffer))
                                self.__add_lexem(ltype = LexemTypes.Variable, lex = len(self.__variables_table) - 1, value = self.__buffer, description = f"variable <{self.__buffer}> of type <{variable_type.value}>")
                                self.__clear_buffer()
                            
                            else:
                                variables_name_table: str = [var.name for var in self.__variables_table]
                                self.__add_lexem(ltype = LexemTypes.Variable, lex = variables_name_table.index(self.__buffer), value = self.__buffer, description =f"variable <{self.__buffer}>")
                                self.__clear_buffer()

                        self.__state = LexemProcessorStates.Idle

                    continue

                case LexemProcessorStates.ReadingNum:
                    if self.__char.isdigit():
                        self.__add_to_buffer(self.__char)
                        self.__get_next_char()
                    
                    elif self.__char == "." and self.__filedata[self.__filedata.index(self.__char) + 1].isdigit():
                        if self.__is_float:
                            self.__state = LexemProcessorStates.Error
                            self.__error = f"[ERROR] Число не может иметь несколько разделителей в виде точки. Отсановка произошла на символе №{self.__pointer}"
                            continue
                        
                        self.__add_to_buffer(self.__char)
                        self.__get_next_char()
                        self.__is_float = True

                    else:
                        if self.__is_float:
                            self.__add_lexem(ltype = LexemTypes.Constant, lex = float(self.__buffer), value = self.__buffer, description = f"float with value = {self.__buffer}")
                            self.__is_float = False

                        else:
                            self.__add_lexem(ltype = LexemTypes.Constant, lex = int(self.__buffer), value = self.__buffer, description = f"int with value = {self.__buffer}")
                        
                        self.__state = LexemProcessorStates.Idle
                    
                    continue

                case LexemProcessorStates.Delimeter:
                    if self.__char in Constants.KeySymbols or self.__char in list(Constants.Operators.keys()) or self.__char in list(Constants.Comparison.keys()):
                        self.__add_to_buffer(input = self.__char)
                        self.__get_next_char()

                    else:
                        search_delimeter =  self.search_in_delimeter_dictionary()
                        search_operation = self.search_in_operations_dictionary()
                        search_comparison = self.search_in_comparison_dictionary()

                        if search_delimeter[0] != -1:
                            self.__add_lexem(ltype = LexemTypes.Delimeter, lex = search_delimeter[0], value = search_delimeter[1])
                            self.__state = LexemProcessorStates.Idle
                            self.__clear_buffer()
                        
                        elif search_operation[0] != -1:
                            self.__add_lexem(ltype = LexemTypes.Operation, lex = search_operation[0], value = search_operation[1])
                            self.__state = LexemProcessorStates.Idle
                            self.__clear_buffer()
                            self.__get_next_char()

                        elif search_comparison[0] != -1:
                            self.__add_lexem(ltype = LexemTypes.Comparison, lex = search_comparison[0], value = search_comparison[1])
                            self.__state = LexemProcessorStates.Idle
                            self.__clear_buffer()
                            self.__get_next_char()
                        
                        else:
                            self.__add_lexem(ltype = LexemTypes.ParsingError, lex = -1, value = "-1", description = f"Ошибка на символе №{self.__pointer}: Не возможно прочитать {self.__buffer}!")
                            self.__state = LexemProcessorStates.Error
                            self.__error = f"Ошибка на символе №{self.__pointer}: Не возможно прочитать {self.__buffer}!"
                    
                    continue
           
                case LexemProcessorStates.ReadingLiteral:
                    if self.__char != self.__buffer[0]:
                        self.__add_to_buffer(input = self.__char)
                        self.__get_next_char()
                    
                    else:
                        self.__add_to_buffer(input = self.__char)
                        self.__add_lexem(LexemTypes.Constant, self.__buffer, f"string with value = {self.__buffer}")
                        self.__clear_buffer()
                        self.__state = LexemProcessorStates.Idle
                        self.__get_next_char()
                    
                        continue

        return (self.__lexems, self.__variables_table) 
    
    def __is_empty_or_next_line(sel, input) -> bool:
        return input == ' ' or input == '\n' or input == '\t' or input == '\0' or input == '\r' 

    def __get_next_char(self):
        self.__pointer += 1
        self.__char = self.__filedata[self.__pointer]

    def __clear_buffer(self):
        self.__buffer = ''

    def search_in_lexem_dictionary(self) -> tuple[int, str]:
        if self.__buffer in Constants.Keywords:
            return (Constants.Keywords.index(self.__buffer), self.__buffer)
        return (-1, self.__buffer)

    def search_in_types_dictionary(self) -> tuple[int, str]:
        if self.__buffer in list(Constants.Types.keys()):
            return Constants.Types[self.__buffer]
        return (-1, self.__buffer)
    
    def search_in_operations_dictionary(self) -> tuple[int, str]:
        if self.__buffer in list(Constants.Operators.keys()):
            return Constants.Operators[self.__buffer]
        return (-1, self.__buffer)
    
    def search_in_delimeter_dictionary(self):
        if self.__buffer in Constants.KeySymbols:
            return (Constants.KeySymbols.index(self.__buffer), self.__buffer)
        return (-1, self.__buffer)
    
    def search_in_comparison_dictionary(self):
        if self.__buffer in list(Constants.Comparison.keys()):
            return Constants.Comparison[self.__buffer]
        return (-1, self.__buffer)

    def __add_to_buffer(self, input):
        self.__buffer += input

    def __add_lexem(self, ltype: LexemTypes, value: int, lex: str, description: str = None):
        if description is None:
            self.__lexems.append(Lexem(ltype = ltype, lex = lex, value = value))
        else:
            self.__lexems.append(Lexem(ltype = ltype, lex = lex, value = value, description = description))

    def __read_file(self, file: str):
        with open(file, 'r', encoding='utf-8') as f:
            return f.read()