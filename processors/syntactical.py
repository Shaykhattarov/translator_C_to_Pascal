from models.token import Token
from constants import Tag


class TreeNode:

    def __init__(self, token: Token, token_type, scope) -> None:
        self.parent = None
        self.token = token
        self.type = token_type
        self.scope = scope


class SyntacticalProcessor:
    __lexems: list[Token]
    __current_token: Token
    __pointer: int = 0


