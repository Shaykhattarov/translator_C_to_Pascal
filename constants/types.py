from models.type import Type
from constants.tag import Tag

class Types:
    Int = Type("int", Tag.INT, 4)
    Float = Type("float", Tag.FLOAT, 8)
    Char = Type("char", Tag.CHAR, 1)
    Bool = Type("bool", Tag.BOOLEAN, 1)
    Array = Type("arr", Tag.ARRAY, 1)
