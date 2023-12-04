from models import Token
from constants.tag import Tag

class Types:
    Int = Token("int", Tag.INT)
    Float = Token("float", Tag.FLOAT)
    Char = Token("char", Tag.CHAR)
    Bool = Token("bool", Tag.BOOLEAN)
    Array = Token("arr", Tag.ARRAY)
