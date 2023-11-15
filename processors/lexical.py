from typing import Union
from models.lexical_processor_states import LexicalProcessorStates
from models.word import Word
from models.type import Type
from models.token import Token
from models import Integer, Float
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
        self.__reserve(Word("{", Tag.OP_BRACES))
        self.__reserve(Word("}", Tag.CL_BRACES))
        self.__reserve(Word("(", Tag.OP_PARENTHESES))
        self.__reserve(Word(")", Tag.CL_PARENTHESES))
        self.__reserve(Word(";", Tag.EOS))
        self.__reserve(Word("=", Tag.ASSIGN))
        self.__reserve(Word("-", Tag.MINUS))
        self.__reserve(Word("+", Tag.PLUS))
        self.__reserve(Word("*", Tag.MULTI))
        self.__reserve(Word("/", Tag.DIVIDE))
        self.__reserve(Word("//", Tag.DIVIDE))
        self.__reserve(Word("++", Tag.INCREMENT))
        self.__reserve(Word("--", Tag.DECREMENT))
        self.__reserve(Word("&&", Tag.AND))
        self.__reserve(Word("||", Tag.OR))
        self.__reserve(Word("==", Tag.EQUAL))
        self.__reserve(Word("!=", Tag.NOT_EQUAL))
        self.__reserve(Word("<=", Tag.LR_EQUAL))
        self.__reserve(Word(">=", Tag.GR_EQUAL))
        self.__reserve(Word("true", Tag.TRUE))
        self.__reserve(Word("false", Tag.FALSE))
        self.__reserve(Word("if", Tag.IF))
        self.__reserve(Word("else", Tag.ELSE))
        self.__reserve(Word("while", Tag.WHILE))
        self.__reserve(Word("do", Tag.DO))
        self.__reserve(Word("break", Tag.BREAK))
        self.__reserve(Word("if", Tag.IF))
        self.__reserve(Word("false", Tag.FALSE))
        self.__reserve(Word("true", Tag.TRUE))
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
                        self.__clear_buffer()
                        self.__add_to_buffer(input = self.__char)
                        self.__state = LexicalProcessorStates.ReadingLiteral
                        self.__get_next_char()
                    
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
                            self.__add_lexem(Float(float(self.__buffer)))
                            self.__clear_buffer()
                            self.__is_float = False

                        else:
                            self.__add_lexem(Integer(int(self.__buffer)))
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
                            self.__add_lexem(Word(self.__buffer, Tag.IDENTIFIER))
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
                            token = Token(self.__buffer)
                            self.__add_lexem(token)
                            self.__clear_buffer()

                        self.__state = LexicalProcessorStates.Idle
                    
                    else:
                        search_keyword = self.search_in_keywords_dictionary()
                        if search_keyword is not None:
                           self.__add_lexem(search_keyword)
                           self.__clear_buffer()
                           self.__get_next_char() 
                        else:
                            token = Token(self.__buffer)
                            self.__add_lexem(token)
                            self.__clear_buffer()

                        self.__state = LexicalProcessorStates.Idle
                    
                    continue

                case LexicalProcessorStates.Error:
                    self.__state = LexicalProcessorStates.Final
                    raise Exception(self.__error)
                    exit()
        
        return self.__lexems

    def __reserve(self, word: Union[Word, Type]):
        self.__keywords[word.lexeme] = word 

    def __is_empty_or_next_line(self, input: str):
        return input == ' ' or input == '\n' or input == '\t' or input == '\0' or input == '\r'

    def __get_next_char(self):
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