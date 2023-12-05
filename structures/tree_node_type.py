

TREE_NODE_TYPE_MNEMONIC = ["UNKNOWN", "MODULE", "CONSTANT", "TYPE", "SYMBOL", "UNARY_OP", "BINARY_OP", "CALL",
        "FUNCTION", "BLOCK", "ASSIGNMENT", "IF_ELSE", "WHILE", "RETURN", "BREAK"]


class TreeNodeType:
    UNKNOWN: int = 0
    MODULE: int = 1
    CONSTANT: int = 2
    TYPE: int = 3
    SYMBOL: int = 4
    UNARY_OP: int = 5
    BINARY_OP: int = 6
    CALL: int = 7
    FUNCTION: int = 8
    BLOCK: int = 9
    ASSIGNMENT: int = 10
    IF_ELSE: int = 11
    WHILE: int = 12
    RETURN: int = 13
    BREAK: int = 14
