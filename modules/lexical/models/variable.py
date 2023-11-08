

class Variable:
    id: int
    type: str
    name: str

    def __init__(self, vid, data_type, name) -> None:
        self.id = vid
        self.type = data_type
        self.name = name

    def to_string(self):
        return f"Variable ID: <{self.id}> Variable of type <{self.type}> with name <{self.name}>"