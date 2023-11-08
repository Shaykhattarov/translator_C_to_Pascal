
class Constants:

    Types: dict[str, tuple] = {
        "int": (0, "32-bit integer"),
		"uint": (1, "32-bit unsigned integer"),
		"long": (2, "64-bit integer"),
		"ulong": (3, "64-bit unsigned integer"),
        "float": (4, "32-bit float"),
		"string": (5, "string of chars"),
        "char": (6, "char")
    }

    Operators: dict[str, tuple] = {
		"+":(0, "sum_operation"),
		"-":(1, "subtract_operation"),
		"*":(2, "multiply_operation"),
		"/":(3, "divide_operation"),
		"+=": (4, "add_amount_operation"),
		"-=": (5, "subtract_amount_operation"),
		"++": (6, "increment_operation"),
		"--": (7, "decrement_operation"),
		"%": (8, "modulo_operation"),
        "**": (9, "degree_operation"),
        "=": (10, "assign_operation")
    }

    Comparison: dict[str, tuple] = {
        "==": (0, "are_equal_comparison"),
        "!=": (1, "nor_equal_comparison"),
		">": (2, "more_comparison"),
		"<": (3, "less_comparison"),
        "<=": (4, "less_or_equal_comparison"),
        ">=": (5, "more_or_equal_comparison")
    }

    Keywords: list[str] = ["for", "if", "else", "while"]

    KeySymbols: list[str] = [".", ";", ",", "(", ")", "[", "]", "{", "}", "()"]
    Literal: list[str] = ["'", '"']



