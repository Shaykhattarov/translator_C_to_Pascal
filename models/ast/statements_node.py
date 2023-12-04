from models.ast import ExpressionNode

class StatementsNode(ExpressionNode):
    code: list[ExpressionNode] = []

    def add_node(self, node: ExpressionNode):
        self.code.append(node)