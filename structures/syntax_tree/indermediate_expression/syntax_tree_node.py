

class SyntaxTreeNode:
    line: int = 0

    def error(self, s: str):
        raise Exception(f"Error around {self.line}: {s}")