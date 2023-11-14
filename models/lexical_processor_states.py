

class LexicalProcessorStates:
    Idle: int = 1
    ReadingNum: int = 2
    Delimeter: int = 3
    Completed: int = 4
    ReadingIdentifier: int = 5
    ReadingLiteral: int = 6
    Assign: int = 7
    Error: int = 8
    Final: int = 9
    ScopeOpened: int = 10
    ScopeClosed: int = 11