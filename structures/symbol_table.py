from models import Symbol, SymbolType, Token

SymbolTypeMnemonic: list = ["UNKNOWN", "CONSTANT", "FUNCTION", "ARGUMENT", "VARIABLE"]


class SymbolTable:
    childs: list = []
    name: str
    symbols: list[Symbol] = []
    arg_count: int = 0

    def __init__(self, name: str = "GLOBAL") -> None:
        self.parent = None
        self.name = name

    def __repr__(self) -> str:
        return f"<SymbolTable {self.name} - {len(self.childs)} - {len(self.symbols)}>"

    def add_child(self, child) -> bool:
        if child is None: return False
        child.parent = self
        self.childs.append(child)
        return True
    
    def remove_child(self, child):
        for entry in self.childs:
            if entry == child:
                self.childs.remove(entry)
                return

    def child_at(self, index: int):
        return self.childs[index]
    
    def get_child_count(self):
        return len(self.childs)
    
    def clear_symbols(self):
        self.symbols = []

    def get_symbols_count(self):
        return len(self.symbols)
    
    def add_symbol(self, token: Token, stype: SymbolType):
        if self.look_up_symbol(token) is not None:
            return False
        
        name = f"{token.lexeme}"
        local_index = self.get_next_index(stype)
        address = 0
        entry: Symbol = Symbol(name, stype, local_index, address)
        self.symbols.append(entry)
        return True


    def get_next_index(self, stype: SymbolType):
        count: int = self.get_symbols_count()
        index = 0
        for i in range(count):
            entry = self.symbols[i]
            if entry.stype == stype:
                index += 1
        return index


    def look_up_symbol(self, token: Token = None, name: str = None, stype: SymbolType = None):
        count: int = self.get_symbols_count()
        
        if token is None and name is not None and stype is not None:
            # Поиск символа в текущем экземпляре
            for i in range(count):
                entry: Symbol = self.symbols[i]
                equal_name: bool = entry.name == name
                if equal_name and entry.stype == stype:
                    return self.symbols[i]    

            # Поиск символа в родительском экземпляре
            if self.parent is not None:
                entry = self.parent.look_up_symbol(name, stype)
                if entry is not None:
                    return entry
                
        if token is not None:
            # Поиск символа в текущем экземпляре
            for i in range(count):
                entry: Symbol = self.symbols[i]
                
                if entry.name == token.lexeme:
                    return self.symbols[i]    

            # Поиск символа в родительском экземпляре
            if self.parent is not None:
                entry = self.parent.look_up_symbol(token)
                if entry is not None:
                    return entry
        
        return None
    
    def print_symbols(self):
        print("-----------------------------------------------------")
        print("Symbol table")
        print("-----------------------------------------------------")
        self.print_recursive(0)

    def print_recursive(self, depth):
        count: int = self.get_symbols_count()
        for i in range(depth):
            print('\t')
        print(f"{self.name}:")
        for i in range(count):
            entry = self.symbols[i]
            for j in range(depth):
                print('\t')
            print(entry.name, end='\t')
            print(SymbolTypeMnemonic[int(entry.stype)], end="")
            if entry.stype == SymbolType.FUNCTION:
                print(f" at [{entry.address}]", end="")
                print(f" args={entry.arg_count}")
            else:
                print(" #", entry.local_index)
            
            print()
        
        for i in range(len(self.childs)):
            self.childs[i].print_recursive(depth + 1)

