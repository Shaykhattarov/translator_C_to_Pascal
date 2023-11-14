from models.type import Type
from constants.tag import Tag

class Types:
    Int = Type("int", Tag.BASIC, 4)
    Float = Type("float", Tag.BASIC, 8)
    Char = Type("char", Tag.BASIC, 1)
    Bool = Type("bool", Tag.BASIC, 1)
    Array = Type("arr", Tag.BASIC, 1)
