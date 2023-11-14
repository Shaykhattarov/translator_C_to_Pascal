from models.word import Word
from constants.tag import Tag

class Words:
    And: Word = Word("&&", Tag.AND)
    Or: Word = Word("||", Tag.OR)
    Eq: Word = Word("==", Tag.EQ)
    Ne: Word = Word("!=", Tag.NE)
    Le: Word = Word("<=", Tag.LE)
    Ge: Word = Word(">=", Tag.GE)
    #Minus: Word = Word("minus", Tag.MINUS)
    true: Word = Word("true", Tag.TRUE)
    false: Word = Word("false", Tag.FALSE)
    #Temp: Word = Word("t", Tag.TEMP)
