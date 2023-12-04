from models.symbol_type import SymbolType



class Symbol:
    name: str = ""
    stype: SymbolType
    local_index: int = -1
    address: int = -1
    arg_count: int = 0