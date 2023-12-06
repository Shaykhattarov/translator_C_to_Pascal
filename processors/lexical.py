from typing import Union
from models.lexical_processor_states import LexicalProcessorStates
from models.token import Token
from constants.tag import Tag
from constants.types import Types


class LexicalProcessor:
    __char: str
    __buffer: str
    __filecontent: str
    __state: int = LexicalProcessorStates.Idle
    __keywords: dict = {}
    __lexems: list[object] = []
    __error: str
    __pointer: int = 0
    __is_float: bool = False

    def __init__(self) -> None:
        self.__reserve(Token("{", Tag.OP_BRACES))
        self.__reserve(Token("}", Tag.CL_BRACES))
        self.__reserve(Token("(", Tag.OP_PARENTHESES))
        self.__reserve(Token(")", Tag.CL_PARENTHESES))
        self.__reserve(Token(">", Tag.GREATER))
        self.__reserve(Token("<", Tag.LOWER))
        self.__reserve(Token(";", Tag.EOS))
        self.__reserve(Token("=", Tag.ASSIGN))
        self.__reserve(Token("-", Tag.MINUS))
        self.__reserve(Token("+", Tag.PLUS))
        self.__reserve(Token("*", Tag.MULTI))
        self.__reserve(Token("/", Tag.DIVIDE))
        self.__reserve(Token("//", Tag.DIVIDE))
        self.__reserve(Token("++", Tag.INCREMENT))
        self.__reserve(Token("--", Tag.DECREMENT))
        self.__reserve(Token("&&", Tag.AND))
        self.__reserve(Token("||", Tag.OR))
        self.__reserve(Token("==", Tag.EQUAL))
        self.__reserve(Token("!=", Tag.NOT_EQUAL))
        self.__reserve(Token("<=", Tag.LR_EQUAL))
        self.__reserve(Token(">=", Tag.GR_EQUAL))
        self.__reserve(Token("true", Tag.TRUE))
        self.__reserve(Token("false", Tag.FALSE))
        self.__reserve(Token("if", Tag.IF))
        self.__reserve(Token("else", Tag.ELSE))
        self.__reserve(Token("while", Tag.WHILE))
        self.__reserve(Token("do", Tag.DO))
        self.__reserve(Token("break", Tag.BREAK))
        self.__reserve(Token("if", Tag.IF))
        self.__reserve(Token("false", Tag.FALSE))
        self.__reserve(Token("true", Tag.TRUE))
        self.__reserve(Types.Int)
        self.__reserve(Types.Float)
        self.__reserve(Types.Char)
        self.__reserve(Types.Array)
        self.__reserve(Types.Bool)

    def process_file(self, file: str):
        self.__filecontent = self.__readfile(filename = file)
        self.__char = self.__filecontent[self.__pointer]

        while self.__state != LexicalProcessorStates.Final and self.__pointer < len(self.__filecontent) - 1:
            match self.__state:
                case LexicalProcessorStates.Final:
                    break

                case LexicalProcessorStates.Idle:
                    if self.__is_empty_or_next_line(input = self.__char):
                        self.__get_next_char()
        
                    elif self.__char.isalpha():
                        self.__clear_buffer()
                        self.__add_to_buffer(input = self.__char)
                        self.__state = LexicalProcessorStates.ReadingIdentifier
                        self.__get_next_char()
                    
                    elif self.__char.isdigit():
                        self.__clear_buffer()
                        self.__add_to_buffer(input = self.__char)
                        self.__state = LexicalProcessorStates.ReadingNum
                        self.__get_next_char()

                    elif self.__char in ["'", '"']:
                        raise Exception("Литералы в данной версии лексического анализатора не поддерживаются")
                        # self.__clear_buffer()
                        # self.__add_to_buffer(input = self.__char)
                        # self.__state = LexicalProcessorStates.ReadingLiteral
                        # self.__get_next_char()
                    
                    else:
                        self.__clear_buffer()
                        self.__state = LexicalProcessorStates.Delimeter
                        self.__add_to_buffer(input = self.__char)
                        self.__get_next_char()
                    
                    continue

                case LexicalProcessorStates.ReadingNum:
                    if self.__char.isdigit():
                        self.__add_to_buffer(self.__char)
                        self.__get_next_char()

                    elif self.__char == ".":
                        if self.__is_float:
                            self.__state = LexicalProcessorStates.Error
                            self.__error = f"[ERROR] Число не может иметь несколько разделителей в виде точки. Остановка произошла на символе №{self.__pointer}"
                            continue
                    
                        self.__add_to_buffer(self.__char)
                        self.__get_next_char()
                        self.__is_float = True
                    
                    else:
                        if self.__is_float:
                            self.__add_lexem(Token(lex=self.__buffer, tag=Tag.CONSTANT))
                            self.__clear_buffer()
                            self.__is_float = False

                        else:
                            self.__add_lexem(Token(lex=self.__buffer, tag=Tag.CONSTANT))
                            self.__clear_buffer()
                        
                        self.__state = LexicalProcessorStates.Idle
                    
                    continue

                case LexicalProcessorStates.ReadingIdentifier:
                    if self.__char.isalpha() or self.__char.isdigit():
                        self.__add_to_buffer(input = self.__char)
                        self.__get_next_char()

                    else:
                        search_keyword = self.search_in_keywords_dictionary()

                        if search_keyword is not None:
                            self.__add_lexem(search_keyword)
                            self.__clear_buffer()

                        else:
                            self.__add_lexem(Token(lex=self.__buffer, tag=Tag.IDENTIFIER))
                            self.__clear_buffer()

                        self.__state = LexicalProcessorStates.Idle

                    continue

                case LexicalProcessorStates.Delimeter:
                    if self.__buffer + self.__char in self.__keywords.keys() and self.__buffer not in ["(", ")", "{", "}"]:
                        self.__add_to_buffer(input = self.__char)
                        
                        search_keyword = self.search_in_keywords_dictionary()
                        if search_keyword is not None:
                            self.__add_lexem(search_keyword)
                            self.__clear_buffer()
                            self.__get_next_char()
                        else:
                            token = Token(self.__buffer, Tag.UNKNOWN)
                            self.__add_lexem(token)
                            self.__clear_buffer()

                        self.__state = LexicalProcessorStates.Idle
                    
                    else:
                        search_keyword = self.search_in_keywords_dictionary()
                        if search_keyword is not None:
                           self.__add_lexem(search_keyword)
                           self.__clear_buffer()
                        else:
                            token = Token(self.__buffer, Tag.UNKNOWN)
                            self.__add_lexem(token)
                            self.__clear_buffer()

                        self.__state = LexicalProcessorStates.Idle
                    
                    continue

                case LexicalProcessorStates.Error:
                    self.__state = LexicalProcessorStates.Final
                    raise Exception(self.__error)
        
        return self.__lexems

    def __reserve(self, word: Token):
        self.__keywords[word.lexeme] = word 

    def __is_empty_or_next_line(self, input: str):
        return input == ' ' or input == '\n' or input == '\t' or input == '\0' or input == '\r'

    def __get_next_char(self):
        #if self.__pointer == len(self.__filecontent):
        #    self.__state = LexicalProcessorStates.Error
        self.__pointer += 1
        self.__char = self.__filecontent[self.__pointer]

    def __add_to_buffer(self, input: str):
        self.__buffer += input

    def __clear_buffer(self):
        self.__buffer = ''

    def __add_lexem(self, obj: object):
        self.__lexems.append(obj)

    def search_in_keywords_dictionary(self):
        if self.__buffer in self.__keywords.keys():
            return self.__keywords[self.__buffer]
        else:
            return None

    def __readfile(self, filename: str):
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()