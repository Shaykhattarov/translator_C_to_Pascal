from models.word import Word
from constants.tag import Tag


class Words:
    And: Word = Word("&&", Tag.AND)
    Or: Word = Word("||", Tag.OR)
    Eq: Word = Word("==", Tag.EQUAL)
    Ne: Word = Word("!=", Tag.NOT_EQUAL)
    Le: Word = Word("<=", Tag.LR_EQUAL)
    Ge: Word = Word(">=", Tag.GR_EQUAL)
    #Minus: Word = Word("minus", Tag.MINUS)
    true: Word = Word("true", Tag.TRUE)
    false: Word = Word("false", Tag.FALSE)
    #Temp: Word = Word("t", Tag.TEMP)
