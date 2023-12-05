from models.symbol_type import SymbolType



class Symbol:
    name: str = ""
    stype: SymbolType
    local_index: int = -1
    address: int = -1
    arg_count: int = 0

    def __init__(self, name: str, stype: SymbolType, local_index: int = -1, address: int = -1, arg_count: int = 0):
        self.name = name
        self.address = address
        self.stype = stype
        self.local_index = local_index
        self.arg_count = arg_count